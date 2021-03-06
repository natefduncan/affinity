from affinity.core import models

def test_persons_list(client):
    persons = client.persons().list()
    assert isinstance(persons["persons"][0], models.Person)

def test_persons_get(client):
    persons = client.persons().list()
    person = client.persons().get(persons["persons"][0].id)
    assert isinstance(person, models.Person)


