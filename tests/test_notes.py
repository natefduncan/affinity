from affinity.core import models


def test_notes_list(client):
    many = client.notes().list()
    assert isinstance(many["notes"][0], models.Note)


def test_notes_get(client):
    many = client.notes().list()
    one = client.notes().get(many["notes"][0].id)
    assert isinstance(one, models.Note)


