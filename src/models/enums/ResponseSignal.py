from enum import Enum

class ResponseSignal(Enum):
    FILE_IS_VALID = "FILE_IS_VALID"
    INVALID_FILE_TYPE = "INVALID_FILE_TYPE"
    INVALID_FILE_SIZE = "INVALID_FILE_SIZE"
    FILE_UPLOAD_FAILED = "FILE_UPLOAD_FAILED"
    FILE_UPLOAD_SUCCESS = "FILE_UPLOAD_SUCCESS"
    FILE_PROCESS_FAILED = "FILE_PROCESS_FAILED"
    NO_FILES_ERROR = "not_found_files"
    FILE_ID_ERROR = "no_file_found_with_this_id"
    
    PROJECT_NOT_FOUND_ERROR = "project_not_found"
    INSERT_INTO_VECTORDB_ERROR = "insert_into_vectordb_error"
    INSERT_INTO_VECTORDB_SUCCESS = "insert_into_vectordb_success"
    VECTORDB_COLLECTION_RETRIEVED = "vectordb_collection_retrieved"
    VECTORDB_SEARCH_ERROR = "vectordb_search_error"
    VECTORDB_SEARCH_SUCCESS = "vectordb_search_success"
    
    

    
