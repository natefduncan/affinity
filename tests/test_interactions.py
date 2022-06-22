from affinity.core import models
from affinity.common.constants import InteractionType
import pytest

@pytest.mark.skip(reason="no way of currently testing this")
def test_interactions_list(client):
    many = client.interactions(type=InteractionType.email).list()
    assert isinstance(many["email"][0], models.EmailInteraction)

