import os
from affinity import Client

AFFINITY_TOKEN = os.getenv("AFFINITY_TOKEN", "") 

def create_opportunity():
    client = Client(AFFINITY_TOKEN)
    test_list = [i for i in client.lists().list() if "Test 2" in i.name][0]
    opportunity = client \
    .opportunities() \
    .create(payload={
        "list_id": test_list.id, 
        "name": "Test Opportunity",
        })
    return opportunity 

def delete_opportunity(opportunity_id):
    client = Client(AFFINITY_TOKEN)
    return client.opportunities().delete(opportunity_id)

def update_opportunity(opportunity_id, payload):
    client = Client(AFFINITY_TOKEN)
    return client.opportunities().update(opportunity_id, payload)

if __name__=="__main__":
   d = create_opportunity()
   update_opportunity(d.id, {"name":"Test Opportunity 2"})
   delete_opportunity(d.id)
