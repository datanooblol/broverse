```mermaid
flowchart TD
    UserInput -->|router| Router
    Router -->|chat| Chat
    Chat -->|continue| UserInput
    Router -->|farewell| Farewell
    Farewell -->|end| End
    UserInput -->|farewell| Farewell
```