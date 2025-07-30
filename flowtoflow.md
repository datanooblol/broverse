```mermaid
flowchart TD
    master_flow -->|default| Router
    Router -->|flow1| Start_flow1
    Start_flow1 -->|default| Start_flow2
    Start_flow2 -->|default| Test5
    Test5 -->|default| End
    Router -->|flow2| Start_flow2
```