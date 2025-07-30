```mermaid
flowchart TD
    Flow_1843592852304 -->|default| Input
    Input -->|default| SystemCommand
    SystemCommand -->|input| Input
    SystemCommand -->|exit| End
    SystemCommand -->|default| ToolSelector
    ToolSelector -->|tool calling| Tools
    Tools -->|default| Chat
    Chat -->|default| Input
    ToolSelector -->|chat| Chat
```