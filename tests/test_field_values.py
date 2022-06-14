from affinity.common.constants import ListType
from affinity.core import models

def test_field_values_list(client):
    many = client.lists().list()
    test_list = [l for l in many if "test" in l.name.lower() and l.type == ListType.organization][0]
    list_entry = client.list_entries(list_id=test_list.id).list()[0]
    field_values = client.field_values().list(organization_id=list_entry.entity_id)
    assert isinstance(field_values[0], models.FieldValue)

