from fastapi import FastAPI
from routes import base, data, nlp
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.vectorDBProviderFactory import VectorDBProviderFactory
from stores.llm.templates.template_parser import TemplateParser

app = FastAPI()

async def startup_span():
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db = app.mongo_conn[settings.MONGODB_DATABASE]

    llm_provider_factory = LLMProviderFactory(settings)
    vectordb_provider_factory = VectorDBProviderFactory(settings)

    # generation client
    app.generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
    if app.generation_client is not None:
        app.generation_client.set_generation_model(model_id = settings.GENERATION_MODEL_ID)
    else:
        print(f"Warning: Generation client could not be created. Check that {settings.GENERATION_BACKEND} is properly configured with required API keys.")

    # embedding client
    app.embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
    if app.embedding_client is not None:
        app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID,
                                                 embedding_size=settings.EMBEDDING_MODEL_SIZE)
    else:
        print(f"Warning: Embedding client could not be created. Check that {settings.EMBEDDING_BACKEND} is properly configured with required API keys.")

    # vector db client
    app.vectordb_client = vectordb_provider_factory.create(
        provider=settings.VECTOR_DB_BACKEND
    )
    if app.vectordb_client is not None:
        app.vectordb_client.connect()
    else:
        print(f"Warning: Vector DB client could not be created. Check that {settings.VECTOR_DB_BACKEND} is properly configured.")

    app.template_parser = TemplateParser(
        language=settings.PRIMARY_LANG,
        default_language=settings.DEFAULT_LANG,
    )


async def shutdown_span():
    app.mongo_conn.close()
    if hasattr(app, 'vectordb_client') and app.vectordb_client is not None:
        app.vectordb_client.disconnect()

app.on_event("startup")(startup_span)
app.on_event("shutdown")(shutdown_span)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)