import os
from affinity import Client
from affinity.common.constants import EntityType, ValueType
import io

AFFINITY_TOKEN = os.getenv("AFFINITY_TOKEN", "") 

def upload_entity_file():
    client = Client(AFFINITY_TOKEN)
    test_list = [i for i in client.lists().list() if "Test 2" in i.name][0]
    opportunity = client.list_entries(list_id=test_list.id).list()[0]
    file = io.BytesIO(b"This is a test file.")
    entity_file = client \
    .entity_files() \
    .upload(opportunity_id = opportunity.entity_id, files={"test.txt": file})
    return entity_file 

if __name__=="__main__":
   d = upload_entity_file()
   
