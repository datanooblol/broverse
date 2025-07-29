from flow import get_flow
import json

if __name__=='__main__':
    flow = get_flow()
    shared = {}
    flow.save_mermaid("./flow.md")
    try:
        flow.run(shared=shared)
    except Exception as e:
        print(e)
        with open('shared.json', 'w') as f:
            json.dump(shared, f, indent=4)
