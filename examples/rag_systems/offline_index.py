from dotenv import load_dotenv
load_dotenv()

import os
from flows.offlineflow import get_offline_flow

if __name__=='__main__':
    flow = get_offline_flow()
    filename = os.path.basename(__file__).replace(".py", ".md")
    filepath = os.path.join(os.path.dirname(__file__), filename)
    flow.save_mermaid(filepath)
    shared = {
        "user_id": "000",
        "username": "admin"
    }
    try:
        flow.run(shared=shared)
    except Exception as e:
        print(str(e))