def test_relationship_strength_list(client):
    persons = client.persons().list()["persons"]
    relationship_strengths = client.relationships_strengths().list(external_id=persons[0].id)
    assert isinstance(relationship_strengths, list)

