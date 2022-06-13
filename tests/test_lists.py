import os
from affinity import Client
from typing import List
from affinity.core import models

AFFINITY_TOKEN = os.getenv("AFFINITY_TOKEN")

def test_lists_list(client):
    assert isinstance(client.lists().list()[0], models.List)

def test_lists_get(client):
    many = client.lists().list()
    one = client.lists().get(many[0].id)
    assert isinstance(one, models.List)
    
def test_list_entries_list(client):
    a = client.lists().list()[0]
    assert isinstance(client.list_entries(list_id=a.id).list()[0], models.ListEntry)

def test_list_entries_get(client):
    a = client.lists().list()[0]
    many = client.list_entries(list_id=a.id).list()
    one = client.list_entries(list_id=a.id).get(many[0].id)
    assert isinstance(one, models.ListEntry)


