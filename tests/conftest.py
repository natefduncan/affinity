import pytest
import os
from affinity import Client
from affinity.common.constants import ListType


@pytest.fixture
def client():
    return Client(os.getenv("AFFINITY_TOKEN", ""))


@pytest.fixture
def opportunity_list(client):
    opportunity_lists = [i for i in client.lists().list() if i.type == ListType.opportunity and "test" in i.name.lower()]
    if opportunity_lists:
        return opportunity_lists[0]
    else:
        raise RuntimeError("Your affinity environment must have an opportunity list for tests to work. The affinity API cannot create lists.")


@pytest.fixture
def organization_list(client):
    organization_lists = [i for i in client.lists().list() if i.type == ListType.organization and "test" in i.name.lower()]
    if organization_lists:
        return organization_lists[0]
    else:
        raise RuntimeError("Your affinity environment must have an organization list for tests to work. The affinity API cannot create lists.")


@pytest.fixture
def person_list(client):
    person_lists = [i for i in client.lists().list() if i.type == ListType.person and "test" in i.name.lower()]
    if person_lists:
        return person_lists[0]
    else:
        raise RuntimeError("Your affinity environment must have a persons list for tests to work. The affinity API cannot create lists.")






