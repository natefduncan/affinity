import os
from affinity import Client
from affinity.common.constants import EntityType, ValueType

AFFINITY_TOKEN = os.getenv("AFFINITY_TOKEN", "") 

def create_note():
    client = Client(AFFINITY_TOKEN)
    test_list = [i for i in client.lists().list() if "Test 2" in i.name][0]
    opportunity = client.list_entries(list_id=test_list.id).list()[0]
    note = client \
    .notes() \
    .create(payload={
        "opportunity_ids" : [opportunity.entity_id],
        "content": "Test Note",
    })
    return note 

def delete_note(note_id):
    client = Client(AFFINITY_TOKEN)
    return client.notes().delete(note_id)

def update_note(note_id, payload):
    client = Client(AFFINITY_TOKEN)
    return client.notes().update(note_id, payload)

if __name__=="__main__":
   d = create_note()
   update_note(d.id, {"content":"Test Note 2"})
   delete_note(d.id)
