from broverse import Action
from broverse.program.dynamodb import update_document_status

class UpdateDocumentStatus(Action):
    def run(self, shared):
        user_id = shared.get("user_id", "000")
        document_id = shared.get("document_id", "")
        update_document_status(
            user_id=user_id, 
            document_id=document_id, 
            new_status="READY"
        )
        shared["action"] = "end"
        return shared