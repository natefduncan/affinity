from affinity.core import models

def test_opportunities_list(client):
    many = client.opportunities().list()
    assert isinstance(many["opportunities"][0], models.Opportunity)

def test_opportunities_get(client):
    many = client.opportunities().list()
    one = client.opportunities().get(many["opportunities"][0].id)
    assert isinstance(one, models.Opportunity)


