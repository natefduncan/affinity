import os
from affinity import Client
from typing import List
from affinity.core import models

AFFINITY_TOKEN = os.getenv("AFFINITY_TOKEN")

def test_opportunities_list():
    client = Client(AFFINITY_TOKEN)
    many = client.opportunities().list()
    assert isinstance(many["opportunities"][0], models.Opportunity)

def test_opportunities_get():
    client = Client(AFFINITY_TOKEN)
    many = client.opportunities().list()
    one = client.opportunities().get(many["opportunities"][0].id)
    assert isinstance(one, models.Opportunity)


