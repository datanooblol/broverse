import os
from broflow.flows.onlineflow import get_online_flow

if __name__=='__main__':
    flow = get_online_flow()
    filename = os.path.basename(__file__).replace(".py", ".md")
    flow.save_mermaid(filename)
    shared = {
        "user_id": "000",
        "username": "admin"
    }
    try:
        flow.run(shared=shared)
    except Exception as e:
        print(str(e))
    print(shared["action"])