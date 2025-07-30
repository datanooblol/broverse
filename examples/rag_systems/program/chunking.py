from broflow.action import Action
from typing import List
from broflow.interface import Context

def split_overlap(contexts:List[Context], max_tokens:int=500, overlap:int=150) -> List[Context]:
    new_contexts:List[Context] = []
    for context in contexts:
        data_content = context.context
        tokens = data_content.split(" ")
        max_len = len(tokens)
        if max_len <= max_tokens:
            new_contexts.append(context)
        else:
            start_idx = 0
            end_idx = max_tokens
            while True:
                new_contexts.append(
                    Context(
                        context=" ".join(tokens[start_idx:end_idx]),
                        metadata=context.metadata
                    )
                )
                if end_idx > max_len:
                    break
                start_idx = end_idx - overlap
                end_idx = start_idx + max_tokens
    for idx in range(len(new_contexts)):
        metadata = new_contexts[idx].metadata.copy()
        metadata['sequence'] = idx
        new_contexts[idx].metadata = metadata
    return new_contexts

class Chunk(Action):
    """Using s3Vector has some limitation on chunk size, but it's easy for the test."""
    def __init__(self, max_tokens:int=150):
        super().__init__()
        self.max_tokens = max_tokens
    def run(self, shared):
        context = shared.get("raw_context", "")
        source = shared.get("source", "")
        context = Context(context=context, metadata={"source": source})
        contexts = split_overlap([context], max_tokens=self.max_tokens, overlap=int(self.max_tokens*0.3))
        shared["contexts"] = contexts
        shared["action"] = "embedding"
        return shared