from .offline.chunking import Chunk
from .offline.uploading import Upload
from .offline.html_parsing import HTMLParsing
from .offline.registering import Register
from .offline.saving_vector_store import SaveVectorStore
from .offline.updating_status import UpdateDocumentStatus
from .both.embedding import OfflineEmbedding
from broflow import Start, End, Flow
from broflow import load_config

def get_offline_flow():
    load_config('examples/rag_systems/config.yml')
    start_action = Start(message="Start of OfflineIndex Flow")
    upload_action = Upload()
    html_parsing = HTMLParsing()
    chunk_action = Chunk()
    register_action = Register()
    embedding_action = OfflineEmbedding()
    save_vector_store_action = SaveVectorStore()
    update_document_status_action = UpdateDocumentStatus()
    end_action = End(message="End of OfflineIndex Flow")
    
    start_action >> upload_action >> register_action
    register_action - "" >> html_parsing >> chunk_action
    chunk_action >> embedding_action >> save_vector_store_action >> update_document_status_action >> end_action
    # upload_action - "register" >> register_action
    # register_action - "html parsing" >> html_parsing
    # html_parsing - "chunk" >> chunk_action
    # chunk_action - "embedding" >> embedding_action
    # embedding_action - "save vectors" >> save_vector_store_action
    # save_vector_store_action - "update status" >> update_document_status_action
    # update_document_status_action - "end" >> end_action

    flow = Flow(start_action=start_action, name="Offline Index")
    return flow