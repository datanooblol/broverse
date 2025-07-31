```mermaid
flowchart TD
    Flow_1691644685648 -->|default| Input
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