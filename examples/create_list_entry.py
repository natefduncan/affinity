import os
from affinity import Client

AFFINITY_TOKEN = os.getenv("AFFINITY_TOKEN", "") 

def create_list_entry():
    client = Client(AFFINITY_TOKEN)
    many = client.lists().list()
    test_list = [l for l in many if l.name.lower() == "test"][0]
    orgs = client.organizations().list()
    list_entry = client \
    .list_entries(list_id=test_list.id) \
    .create(data={
        "entity_id": orgs["organizations"][0].id
    })
    return {
            "list_id" : test_list.id, 
            "list_entry_id" : list_entry.id 
            }

def delete_list_entry(list_id, list_entry_id):
    client = Client(AFFINITY_TOKEN)
    return client.list_entries(list_id=list_id).delete(list_entry_id)
    

if __name__=="__main__":
   d = create_list_entry()
   #  delete_list_entry(d["list_id"], d["list_entry_id"])
