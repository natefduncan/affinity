import os
from affinity import Client
from typing import List
from affinity.core import models

AFFINITY_TOKEN = os.getenv("AFFINITY_TOKEN")

def test_fields_list():
    client = Client(AFFINITY_TOKEN)
    assert isinstance(client.fields.list()[0], models.Field)

