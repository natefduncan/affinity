import os
import pathlib
from pathlib import Path

from affinity.core import models

# from definitions import ROOT_DIR
ROOT_DIR = pathlib.Path(__file__).parent.parent.absolute()

def test_entity_files_list(client):
    many = client.entity_files().list()
    assert isinstance(many["entity_files"][0], models.EntityFile)

def test_entity_files_get(client):
    many = client.entity_files().list()
    one = client.entity_files().get(many["entity_files"][0].id)
    assert isinstance(one, models.EntityFile)

def test_entity_files_download(client):
    many = client.entity_files().list()
    file_path = Path(ROOT_DIR) / many["entity_files"][0].name
    one = client.entity_files().download(many["entity_files"][0].id, file_path)
    assert os.path.exists(file_path)
    os.remove(file_path)
