from affinity.core import models


def test_organizations_list(client):
    many = client.organizations().list()
    assert isinstance(many["organizations"][0], models.Organization)


def test_organizations_get(client):
    many = client.organizations().list()
    one = client.organizations().get(many["organizations"][0].id)
    assert isinstance(one, models.Organization)


def test_organizations_get_with_params(client):
    many = client.organizations().list()
    one = client.organizations().get(
        many["organizations"][0].id,
        with_interaction_dates=True,
        with_interaction_persons=True,
        with_opportunities=True
    )

    assert isinstance(one, models.Organization)


def test_organizations_get_by_domain(client):
    one = client.organizations().get_by_domain("affinity.co")
    assert isinstance(one, models.Organization)


