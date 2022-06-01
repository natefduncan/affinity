import os
from affinity import Client
from typing import List
from affinity.core.models import List

AFFINITY_TOKEN = os.getenv("AFFINITY_TOKEN")

def test_lists_list():
    client = Client(AFFINITY_TOKEN)
    assert isinstance(client.lists.list()[0], List)
