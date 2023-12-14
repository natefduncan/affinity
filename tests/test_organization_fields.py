from affinity.core import models


def test_organization_fields(client):
    many = client.organizations().fields()
    assert isinstance(many[0], models.OrganizationFields)



