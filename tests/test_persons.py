import os
from affinity import Client
from typing import List
from affinity.core import models

AFFINITY_TOKEN = os.getenv("AFFINITY_TOKEN")

def test_persons_list():
    client = Client(AFFINITY_TOKEN)
    persons = client.persons().list()
    assert isinstance(persons["persons"][0], models.Person)

