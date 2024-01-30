from affinity.core import models


def test_persons_list(client):
    persons = client.persons().list()
    assert isinstance(persons["persons"][0], models.Person)


def test_persons_get(client):
    persons = client.persons().list()
    person = client.persons().get(persons["persons"][0].id)
    assert isinstance(person, models.Person)


def test_persons_get_with_params(client):
    persons = client.persons().list()
    person = client.persons().get(
        persons["persons"][0].id,
        with_interaction_dates=True,
        with_opportunities=True,
        with_current_organizations=True,
        with_interaction_persons=True,
    )
    assert person.current_organization_ids is not None
    assert person.interaction_dates is not None
    assert person.interactions is not None
    assert isinstance(person, models.Person)


def test_persons_fields(client):
    many = client.persons().fields()
    assert isinstance(many[0], models.PersonFields)



