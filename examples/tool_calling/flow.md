```mermaid
flowchart TD
    Flow_2607766461712 -->|default| Input
    Input -->|default| SystemCommand
    SystemCommand -->|input| Input
    SystemCommand -->|exit| End
    SystemCommand -->|default| ToolSelector
    ToolSelector -->|tool calling| Tools
    Tools -->|default| Chat
    Chat -->|default| Input
    Tools -->|input| Input
    ToolSelector -->|chat| Chat
```