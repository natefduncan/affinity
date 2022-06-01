import os
from affinity import Client

AFFINITY_TOKEN = os.getenv("AFFINITY_TOKEN")

def test_lists_list():
    client = Client(AFFINITY_TOKEN)
    assert client.lists.list().status_code == 200
