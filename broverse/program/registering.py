from broverse import Action
from uuid import uuid4
from broverse.program.dynamodb import (
    create_document, 
    update_document_status, 
    delete_document, 
    get_user_documents, get_document
)

class Register(Action):
    def run(self, shared):
        user_id = shared.get("user_id", "000")
        username= shared.get("username", "admin")
        source = shared.get("source", "missing")
        document_id = str(uuid4())
        shared["document_id"] = document_id
        vector_path = f"s3://test-vector/{document_id}"
        create_document(
            user_id=user_id,
            document_id=document_id,
            username=username,
            source=source,
            vector_path=vector_path,
            status="CREATED",
        )
        document_type = shared.get("document_type", "")
        shared["action"] = self.get_action(document_type=document_type)
        return shared

    def get_action(self, document_type:str):
        if document_type=="url":
            return "html parsing"
        if document_type=="pdf":
            return "pdf parsing"
        if document_type=="docx":
            return "docx parsing"
        raise ValueError(f"{document_type} is not implemented, try url, pdf, docx.")