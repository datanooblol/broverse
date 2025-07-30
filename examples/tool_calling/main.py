from flow import get_flow
import json

if __name__=='__main__':
    path_dir = "./examples/tool_calling"
    flow = get_flow()
    shared = {}
    flow.save_mermaid(f"{path_dir}/flow.md")
    try:
        flow.run(shared=shared)
    except Exception as e:
        print(e)
        with open(f'{path_dir}/shared.json', 'w') as f:
            json.dump(shared, f, indent=4)
