from broflow.program import (
    Upload, 
    Register, 
    HTMLParsing, 
    Chunk, 
    OfflineEmbedding, 
    SaveVectorStore, 
    UpdateDocumentStatus
)
from broflow import End, Flow


def get_offline_flow():
    upload_action = Upload()
    html_parsing = HTMLParsing()
    chunk_action = Chunk()
    register_action = Register()
    embedding_action = OfflineEmbedding()
    save_vector_store_action = SaveVectorStore()
    update_document_status_action = UpdateDocumentStatus()
    ending_message = "End of OfflineIndex Flow"

    upload_action - "register" >> register_action
    register_action - "html parsing" >> html_parsing
    html_parsing - "chunk" >> chunk_action
    chunk_action - "embedding" >> embedding_action
    embedding_action - "save vectors" >> save_vector_store_action
    save_vector_store_action - "update status" >> update_document_status_action
    update_document_status_action - "end" >> End(message=ending_message)

    flow = Flow(start_action=upload_action)
    return flow