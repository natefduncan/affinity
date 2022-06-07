import os
from affinity import Client
from affinity.common.constants import EntityType, ValueType
from affinity.core import models

AFFINITY_TOKEN = os.getenv("AFFINITY_TOKEN", "") 

def create_field(list_id):
    client = Client(AFFINITY_TOKEN)
    field = client \
    .fields() \
    .create(payload={
        "name": "Test Field",
        "entity_type": EntityType.organization, 
        "value_type": ValueType.text, 
        "list_id": list_id, 
        "is_list_specific" : True
        })
    return field

def create_field_value(field_id, list_entry_id, entity_id):
   client = Client(AFFINITY_TOKEN)
   return client.field_values().create({
       "field_id" : field_id, 
       "entity_id" : entity_id,
       "list_entry_id" : list_entry_id, 
       "value" : "Test Field Value"
    })
      
def update_field_value(field_value_id):
    client = Client(AFFINITY_TOKEN)
    return client.field_values().update(field_value_id, payload={"value": "Test Field Value 2"})

def delete_field(field_id):
    client = Client(AFFINITY_TOKEN)
    return client.fields().delete(field_id)    

def delete_field_value(field_value_id):
    client = Client(AFFINITY_TOKEN)
    client.field_values().delete(field_value_id)

if __name__=="__main__":
    client = Client(AFFINITY_TOKEN)
    many = client.lists().list()
    test_list = [l for l in many if l.name.lower() == "test"][0]
    list_entry = client.list_entries(list_id=test_list.id).list()[0]
    # Create
    field = create_field(test_list.id)
    field_value = create_field_value(field.id, list_entry.id, list_entry.entity_id)
    print(field_value)
    # Update
    updated_field_value = update_field_value(field_value.id)
    print(updated_field_value)
    # Delete
    delete_field_value(field_value.id)
    delete_field(field.id)

    
   #  delete_field(d.id)
