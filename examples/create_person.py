import os
from affinity import Client
from affinity.common.constants import EntityType, ValueType

AFFINITY_TOKEN = os.getenv("AFFINITY_TOKEN", "") 

def create_person():
    client = Client(AFFINITY_TOKEN)
    person = client \
    .persons() \
    .create(
        first_name="Test",
        last_name="Person", 
        emails= ["test@email.com"]
        )
    return person 

def delete_person(person_id):
    client = Client(AFFINITY_TOKEN)
    return client.persons().delete(person_id)

def update_person(person_id, payload):
    client = Client(AFFINITY_TOKEN)
    return client.persons().update(person_id, payload)

if __name__=="__main__":
   d = create_person()
   update_person(d.id, {"last_name":"Person2"})
   delete_person(d.id)
