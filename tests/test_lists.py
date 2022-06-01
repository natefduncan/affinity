import os
from affinity import Client
from typing import List
from affinity.core import models

AFFINITY_TOKEN = os.getenv("AFFINITY_TOKEN")

def test_lists_list():
    client = Client(AFFINITY_TOKEN)
    assert isinstance(client.lists.list()[0], models.List)

def test_lists_get():
    client = Client(AFFINITY_TOKEN)
    many = client.lists.list()
    one = client.lists.get(many[0].id)
    assert isinstance(one, models.List)
    
def test_list_entries_list():
    client = Client(AFFINITY_TOKEN)
    a = client.lists.list()[0]
    print(a)
    assert isinstance(client.list_entries(list_id=a.id).list()[0], models.ListEntry)


