import os
from affinity import Client
from affinity.common.constants import EntityType, ValueType

AFFINITY_TOKEN = os.getenv("AFFINITY_TOKEN", "") 

def create_organization():
    client = Client(AFFINITY_TOKEN)
    organization = client \
    .organizations() \
    .create(payload={
        "name": "Test Organization",
        })
    return organization 

def delete_organization(organization_id):
    client = Client(AFFINITY_TOKEN)
    return client.organizations().delete(organization_id)

def update_organization(organization_id, payload):
    client = Client(AFFINITY_TOKEN)
    return client.organizations().update(organization_id, payload)

if __name__=="__main__":
   d = create_organization()
   update_organization(d.id, {"name":"Test Organization 2"})
   delete_organization(d.id)
