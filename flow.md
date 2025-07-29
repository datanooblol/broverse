```mermaid
flowchart TD
    Start -->|input| Input
    Input -->|continue| SystemCommand
    SystemCommand -->|continue| ToolSelector
    ToolSelector -->|tool calling| Tools
    Tools -->|chat| Chat
    Chat -->|continue| Input
    Tools -->|continue| Input
    ToolSelector -->|chat| Chat
    SystemCommand -->|system_command| Tools
    SystemCommand -->|end| End
```