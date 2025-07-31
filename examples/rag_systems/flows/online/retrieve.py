from broflow import Action
from ..both.s3vector import query_from_s3_vectors

class Retrieve(Action):
    def run(self, shared:dict):
        vector = shared.get("vector", [])
        contexts = query_from_s3_vectors(vector=vector)
        self.print("SOURCE:\n\n{contexts}".format(contexts="\n".join([c.metadata['source']for c in contexts])))
        shared["contexts"] = contexts
        return shared