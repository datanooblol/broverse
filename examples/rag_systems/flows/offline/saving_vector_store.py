from broflow import Action
from ..both.s3vector import save_to_s3_vectors

class SaveVectorStore(Action):
    def run(self, shared):
        contexts = shared.get("contexts")
        vectors = shared.get("vectors")
        save_to_s3_vectors(contexts=contexts, vectors=vectors)
        return shared