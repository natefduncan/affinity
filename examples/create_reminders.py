import os
from affinity import Client
from affinity.common.constants import ReminderType

AFFINITY_TOKEN = os.getenv("AFFINITY_TOKEN", "") 

def create_reminder():
    client = Client(AFFINITY_TOKEN)
    test_list = [i for i in client.lists().list() if "Test 2" in i.name][0]
    opportunity = client.list_entries(list_id=test_list.id).list()[0]
    owner = client.whoami().get()
    reminder = client \
    .reminders() \
    .create(
        content="Test Reminder",
        type=ReminderType.one_time,
        due_date="2022-12-31", 
        opportunity_id=opportunity.entity_id, 
        owner_id=owner["user"]["id"]
    )
    return reminder 

def delete_reminder(reminder_id):
    client = Client(AFFINITY_TOKEN)
    return client.reminders().delete(reminder_id)

def update_reminder(reminder_id, content):
    client = Client(AFFINITY_TOKEN)
    return client.reminders().update(reminder_id, content=content)

if __name__=="__main__":
   d = create_reminder()
   update_reminder(d.id, content="Test Reminder 2")
   delete_reminder(d.id)
