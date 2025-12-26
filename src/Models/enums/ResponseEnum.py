from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATE_SUCCESS ="file_validate_success"
    FILE_TYPE_NOT_SUPPORTED ="file_type_not-supported"
    FILE_SIZE_EXCEEDED ="file_size_exceeded"
    FILE_UPLOADED_Success="file_uploaded_success"
    FILE_UPLOADED_FAILED = "file_uploaded_failed"
    PROCESSING_SUCCESS ="processing_success"
    PROCESSING_FAILED ="processing_failed"
    NO_FILE_ERROR ="not_found_file"
    FILE_ID_ERROR ="not_file_found_with_this_id "
    PROJECT_NOT_FOUND_ERROR ="project_not_found"
    RESPONSE_FAILED ="response_failed"
    RESPONSE_SUCCESS="file_uploaded_success"
    RESPONSE_NOT_UPLOADED_FILE="No_uploaded_file_found_for_this_project"
    RESPONSE_NOT_DOWNLOAD_FILE="Not_download_this_file_from_S3_please_back_to_solve_this_problem."
    
   
    
    