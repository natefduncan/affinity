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
    )
    assert person.current_organization_ids is not None and len(person.current_organization_ids) > 0
    assert person.interaction_dates is not None and len(person.interaction_dates) > 0
    assert person.interactions is not None and  len(person.interactions) > 0
    assert isinstance(person, models.Person)


