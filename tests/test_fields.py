from affinity.core import models

def test_fields_list(client):
    assert isinstance(client.fields().list()[0], models.Field)

