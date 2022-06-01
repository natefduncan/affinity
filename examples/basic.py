import os
from affinity import Client

AFFINITY_TOKEN = os.getenv("AFFINITY_TOKEN", "") 

if __name__=="__main__":
    client = Client(AFFINITY_TOKEN)
    print(client.lists.list())
