from typing import List, Optional, Dict
from affinity.core.models import *
from affinity.client.endpoints import Lists

class Client:
    def __init__(self, token: str):
        self.token = token
        
    @property
    def lists(self):
        return Lists(self.token)
