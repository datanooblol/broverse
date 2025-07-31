from broflow import Action
from broflow.interface import Context

from sentence_transformers import SentenceTransformer

# the embedding dimension: 384
model = SentenceTransformer('all-MiniLM-L6-v2')

class OfflineEmbedding(Action):
    def run(self, shared):
        contexts:list[Context] = shared.get("contexts", [])
        vectors = model.encode([context.context for context in contexts])
        shared["vectors"] = vectors
        return shared
    
class OnlineEmbedding(Action):
    def run(self, shared):
        query = shared.get("user_input", "")
        vector = model.encode([query])[0]
        shared["vector"] = vector
        return shared