# Persona
You are an AI coding assistant and your job is to help me build a library called broverse.  

## Instructions
What broverse does is:  
- using DSL (domain specific language) almost similar to cypher: (source)-[relationship]->(target), but broverse using source-["relationship"]>>target
- source and target's relationships can be: source_a, source_b or source_n connect to target_a. Also, source_a can connect to source_a, source_b or source_n
- I'll giving you a code example as in codebase.py, but we don't have to follow them all. we need to make only match with our use case only

## Developing (I want you to help me with this section)
- Nothing for now

## Current state 
- broverse/action.py is for create an action class which can be combined and using with Flow
- broverse/flow.py is for flow control. Also it can save and display the flow in mermaid diagram
- Simple flow: a1 >> a2 >> a3 is now available
- Complex flows: flow1(a1>>a2>>a3) >> flow2(a4>>a5>>a6) is also available
- prompt is now using file.yaml and load it as raw because it's easy to read and edit
- examples: tool_calling (done)
