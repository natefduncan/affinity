import os
from affinity import Client
from typing import List
from affinity.core import models
from affinity.common.constants import InteractionType
import pytest

AFFINITY_TOKEN = os.getenv("AFFINITY_TOKEN")

@pytest.mark.skip(reason="no way of currently testing this")
def test_interactions_list():
    client = Client(AFFINITY_TOKEN)
    many = client.interactions(type=InteractionType.email).list()
    assert isinstance(many["email"][0], models.EmailInteraction)

