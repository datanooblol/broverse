```mermaid
flowchart TD
    Offline_Index -->|default| Upload
    Upload -->|default| Register
    Register -->|default| HTMLParsing
    HTMLParsing -->|default| Chunk
    Chunk -->|default| OfflineEmbedding
    OfflineEmbedding -->|default| SaveVectorStore
    SaveVectorStore -->|default| UpdateDocumentStatus
    UpdateDocumentStatus -->|default| End
```