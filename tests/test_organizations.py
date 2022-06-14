from affinity.core import models

def test_organizations_list(client):
    many = client.organizations().list()
    assert isinstance(many["organizations"][0], models.Organization)

def test_organizations_get(client):
    many = client.organizations().list()
    one = client.organizations().get(many["organizations"][0].id)
    assert isinstance(one, models.Organization)


