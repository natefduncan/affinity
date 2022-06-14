from affinity.core import models

def test_list_entries_list(client):
    a = client.lists().list()[0]
    assert isinstance(client.list_entries(list_id=a.id).list()[0], models.ListEntry)

def test_list_entries_get(client):
    a = client.lists().list()[0]
    many = client.list_entries(list_id=a.id).list()
    one = client.list_entries(list_id=a.id).get(many[0].id)
    assert isinstance(one, models.ListEntry)

def test_list_entries_create_delete(client, organization_list):
    orgs = client.organizations().list()
    list_entry = client \
            .list_entries(list_id=organization_list.id) \
            .create(entity_id=orgs["organizations"][0].id)
    client.list_entries(list_id=organization_list.id).delete(list_entry.id)
