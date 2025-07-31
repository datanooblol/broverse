from broflow.action import Action

class Upload(Action):
    def run(self, shared:dict):
        document_type = input("Enter your document type: ")
        shared["document_type"] = document_type
        file_path = input("Enter your file path: ")
        shared["source"] = file_path
        return shared