import boto3
from uuid import uuid4
from broverse.interface import Context
import os

s3vectors = boto3.client('s3vectors', region_name='us-west-2')
VECTOR_BUCKET = os.getenv("VECTOR_BUCKET", "test-broverse-20250729")
VECTOR_INDEX = os.getenv("VECTOR_INDEX", "test-url-index")

def save_to_s3_vectors(contexts, vectors):
    embedding_vectors = []
    enum = 0
    for context, vector in zip(contexts, vectors):
        key = str(uuid4())
        metadata = context.metadata.copy()
        metadata['source_text'] = context.context
        metadata['id'] = key
        obj = {
            "key": key, 
            "data": {"float32": vector.tolist()}, 
            "metadata": metadata
        }
        embedding_vectors.append(obj)
        enum += 1
    response = s3vectors.put_vectors(vectorBucketName=VECTOR_BUCKET,
        indexName=VECTOR_INDEX, 
        vectors=embedding_vectors,
    )
    return response

def s3_to_contexts(response):
    contexts = []
    for res in response:
        metadata = res.get("metadata")
        context = metadata.pop("source_text")
        contexts.append(
            Context(context=context, metadata=metadata)
        )
    return contexts

def query_from_s3_vectors(vector, filter=None):
    query = s3vectors.query_vectors(vectorBucketName=VECTOR_BUCKET,
        indexName=VECTOR_INDEX,
        queryVector={"float32":vector},
        topK=10, 
        filter=filter,
        returnDistance=True,
        returnMetadata=True
    )
    results = query["vectors"]
    contexts = s3_to_contexts(results)
    return contexts