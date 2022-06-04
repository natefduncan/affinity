from typing import List, Optional, Dict
from affinity.core.models import *
from affinity.client.endpoints import Lists, ListEntries, Fields

class Client:
    def __init__(self, token: str):
        self.token = token
        
    @property
    def lists(self):
        return Lists(self.token)

    def list_entries(self, list_id: int):
        return ListEntries(token=self.token, list_id=list_id)

    @property
    def fields(self):
        return Fields(self.token)
