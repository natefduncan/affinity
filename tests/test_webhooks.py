import os
from affinity import Client
from typing import List
from affinity.core import models

AFFINITY_TOKEN = os.getenv("AFFINITY_TOKEN")

def test_webhooks_list():
    client = Client(AFFINITY_TOKEN)
    many = client.webhooks().list()
    assert isinstance(many, list)
