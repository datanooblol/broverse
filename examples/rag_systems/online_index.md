```mermaid
flowchart TD
    Online_Flow -->|default| UserInput
    UserInput -->|default| Router
    Router -->|default| Chat
    Chat -->|default| UserInput
    Router -->|farewell| Farewell
    Farewell -->|default| End
    UserInput -->|farewell| Farewell
```