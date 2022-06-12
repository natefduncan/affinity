import os
from affinity import Client
from affinity.common.constants import EntityType, ValueType

AFFINITY_TOKEN = os.getenv("AFFINITY_TOKEN", "") 

def create_field():
    client = Client(AFFINITY_TOKEN)
    many = client.lists().list()
    test_list = [l for l in many if l.name.lower() == "test"][0]
    field = client \
    .fields() \
    .create(
        name="Test Field",
        entity_type=EntityType.organization, 
        value_type=ValueType.text, 
        list_id=test_list.id
        )
    return field

def delete_field(field_id):
    client = Client(AFFINITY_TOKEN)
    return client.fields().delete(field_id)    

if __name__=="__main__":
   d = create_field()
   delete_field(d.id)
