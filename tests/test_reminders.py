from affinity.core import models

def test_reminders_list(client):
    many = client.reminders().list()
    assert isinstance(many["reminders"][0], models.Reminder)

def test_reminders_get(client):
    many = client.reminders().list()
    one = client.reminders().get(many["reminders"][0].id)
    assert isinstance(one, models.Reminder)


