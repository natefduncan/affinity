from affinity.core import models


def test_lists_list(client):
    assert isinstance(client.lists().list()[0], models.List)


def test_lists_get(client):
    many = client.lists().list()
    one = client.lists().get(many[0].id)
    assert isinstance(one, models.List)
