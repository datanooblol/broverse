```mermaid
flowchart TD
    Upload -->|register| Register
    Register -->|html parsing| HTMLParsing
    HTMLParsing -->|chunk| Chunk
    Chunk -->|embedding| OfflineEmbedding
    OfflineEmbedding -->|save vectors| SaveVectorStore
    SaveVectorStore -->|update status| UpdateDocumentStatus
    UpdateDocumentStatus -->|end| End
```