import os
from affinity import Client

AFFINITY_TOKEN = os.getenv("AFFINITY_TOKEN")

def test_lists_list():
    client = Client(AFFINITY_TOKEN)
    assert client.lists.list().response_code == 200
