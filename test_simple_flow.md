```mermaid
flowchart TD
    InputAction -->|router| RouterAction
    RouterAction -->|chat| ChatAction
    ChatAction -->|continue| InputAction
    RouterAction -->|farewell| FarewellAction
    FarewellAction -->|end| End
    InputAction -->|end| End
```