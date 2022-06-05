import os
from affinity import Client
from typing import List
from affinity.core import models
from affinity.common.constants import InteractionType

AFFINITY_TOKEN = os.getenv("AFFINITY_TOKEN")

def test_interactions_list():
    client = Client(AFFINITY_TOKEN)
    many = client.interactions(type=InteractionType.email).list()
    assert isinstance(many["email"][0], models.EmailInteraction)

