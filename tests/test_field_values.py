from affinity.core import models

def test_field_values_list(client, organization_list):
    list_entry = client.list_entries(list_id=organization_list.id).list()[0]
    field_values = client.field_values().list(organization_id=list_entry.entity_id)
    assert isinstance(field_values[0], models.FieldValue)

