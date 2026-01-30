from .BaseController import BaseController
from models.db_schema import Project, DataChunk
from stores.llm.LLMEnum import DocumentTypeEnum
from typing import List
import json
import logging

logger = logging.getLogger(__name__)

class NLPController(BaseController):

    def __init__(self, vectordb_client, generation_client, 
                 embedding_client, template_parser):
        super().__init__()

        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client
        self.template_parser = template_parser

    def create_collection_name(self, project_id: str):
        return f"collection_{project_id}".strip()
    
    def reset_vector_db_collection(self, project: Project):
        if not self.vectordb_client:
            logger.error("Vector DB client was not set")
            return False
        collection_name = self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.delete_collection(collection_name=collection_name)
    
    def get_vector_db_collection_info(self, project: Project):
        if not self.vectordb_client:
            logger.error("Vector DB client was not set")
            return None
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = self.vectordb_client.get_collection_info(collection_name=collection_name)

        return json.loads(
            json.dumps(collection_info, default=lambda x: x.__dict__)
        )
    
    def index_into_vector_db(self, project: Project, chunks: List[DataChunk],
                                   chunks_ids: List[int], 
                                   do_reset: bool = False):

        if not self.vectordb_client:
            logger.error("Vector DB client was not set")
            return False

        if not self.embedding_client:
            logger.error("Embedding client was not set")
            return False
        
        # step1: get collection name
        collection_name = self.create_collection_name(project_id=project.project_id)

        # step2: manage items
        texts = [ c.chunk_text for c in chunks ]
        metadata = [ c.chunk_metadata for c in  chunks]
        vectors = [
            self.embedding_client.embed_text(text=text, 
                                             document_type=DocumentTypeEnum.DOCUMENT.value)
            for text in texts
        ]

        # step3: create collection if not exists
        created = self.vectordb_client.create_collection(
            collection_name=collection_name,
            embedding_size=self.embedding_client.embedding_size,
            do_reset=do_reset,
        )
        if created is False:
            logger.error("Failed to create or validate vector db collection")
            return False

        # step4: insert into vector db
        inserted = self.vectordb_client.insert_many(
            collection_name=collection_name,
            texts=texts,
            metadata=metadata,
            vectors=vectors,
            record_ids=chunks_ids,
        )
        if inserted is False:
            logger.error("Failed to insert vectors into vector db")
            return False

        return True

    def search_vector_db_collection(self, project: Project, text: str, limit: int = 10):

        # step1: get collection name
        collection_name = self.create_collection_name(project_id=project.project_id)

        if not self.vectordb_client:
            logger.error("Vector DB client was not set")
            return False

        if not self.embedding_client:
            logger.error("Embedding client was not set")
            return False

        # step2: get text embedding vector
        vector = self.embedding_client.embed_text(text=text, 
                                                 document_type=DocumentTypeEnum.QUERY.value)

        if not vector or len(vector) == 0:
            last_error = getattr(self.embedding_client, "last_error_type", None)
            if last_error == "rate_limit":
                return {"error": "rate_limit"}
            if last_error == "api":
                return {"error": "api"}
            return False

        # step3: do semantic search
        results = self.vectordb_client.search_by_vector(
            collection_name=collection_name,
            vector=vector,
            limit=limit
        )

        if not results:
            return False

        return results
    
    def answer_rag_question(self, project: Project, query: str, limit: int = 10):
        
        answer, full_prompt, chat_history = None, None, None

        if not self.vectordb_client:
            logger.error("Vector DB client was not set")
            return answer, full_prompt, chat_history

        if not self.embedding_client or not self.generation_client:
            logger.error("Embedding or generation client was not set")
            return answer, full_prompt, chat_history

        # step1: retrieve related documents
        retrieved_documents = self.search_vector_db_collection(
            project=project,
            text=query,
            limit=limit,
        )

        # Check if search returned an error object
        if isinstance(retrieved_documents, dict) and "error" in retrieved_documents:
            # Handle search errors by returning an appropriate response
            system_prompt = self.template_parser.get("rag", "system_prompt")
            footer_prompt = self.template_parser.get("rag", "footer_prompt", {"query": query})

            # Create a prompt that indicates there was a search error
            documents_prompts = f"An error occurred while searching for relevant documents: {retrieved_documents.get('error', 'Unknown error')}"
            full_prompt = "\n\n".join([documents_prompts, footer_prompt])

            # step3: Construct Generation Client Prompts
            chat_history = [
                self.generation_client.construct_prompt(
                    prompt=system_prompt,
                    role="system",
                )
            ]

            # step4: Retrieve the Answer
            answer = self.generation_client.generate_text(
                prompt=full_prompt,
                chat_history=chat_history
            )

            # If the LLM failed to generate an answer, return a default message
            if not answer:
                error_msg = retrieved_documents.get('error', 'Unknown error') if isinstance(retrieved_documents, dict) else 'Unknown error'
                answer = f"Sorry, I couldn't generate an answer for your query: '{query}'. An error occurred while searching for documents: {error_msg}"

            return answer, full_prompt, chat_history

        if not retrieved_documents or len(retrieved_documents) == 0:
            # If no documents are retrieved, we still want to try to generate an answer
            # but with an indication that no supporting documents were found
            system_prompt = self.template_parser.get("rag", "system_prompt")

            # Create a prompt that indicates no documents were found
            documents_prompts = "No relevant documents were found in the knowledge base to answer this query."
            footer_prompt = self.template_parser.get("rag", "footer_prompt", {"query": query})

            # step3: Construct Generation Client Prompts
            chat_history = [
                self.generation_client.construct_prompt(
                    prompt=system_prompt,
                    role="system",
                )
            ]

            full_prompt = "\n\n".join([documents_prompts, footer_prompt])

            # step4: Retrieve the Answer
            answer = self.generation_client.generate_text(
                prompt=full_prompt,
                chat_history=chat_history
            )

            # If the LLM failed to generate an answer, return a default message
            if not answer:
                answer = f"Sorry, I couldn't generate an answer for your query: '{query}'. No relevant documents were found in the knowledge base."

            return answer, full_prompt, chat_history
        
        # step2: Construct LLM prompt
        system_prompt = self.template_parser.get("rag", "system_prompt")

        documents_prompts = "\n".join([
            self.template_parser.get("rag", "document_prompt", {
                    "doc_num": idx + 1,
                    "chunk_text": doc,
            })
            for idx, doc in enumerate(retrieved_documents)
        ])

        footer_prompt = self.template_parser.get("rag", "footer_prompt", {"query": query})

        # step3: Construct Generation Client Prompts
        # Use "system" role directly as OpenAI expects this value
        chat_history = [
            self.generation_client.construct_prompt(
                prompt=system_prompt,
                role="system",
            )
        ]

        full_prompt = "\n\n".join([ documents_prompts,  footer_prompt])

        # step4: Retrieve the Answer
        answer = self.generation_client.generate_text(
            prompt=full_prompt,
            chat_history=chat_history
        )

        # If the LLM failed to generate an answer, return a default message
        if not answer:
            answer = f"Sorry, I couldn't generate an answer for your query: '{query}'. This might be due to an issue with the language model service."

        return answer, full_prompt, chat_history

