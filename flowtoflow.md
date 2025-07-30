```mermaid
flowchart TD
    master_flow -->|default| Start flow1
    Start flow1 -->|default| Start flow2
    Start flow2 -->|default| Test5
    Test5 -->|default| End
```