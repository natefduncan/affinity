def test_webhooks_list(client):
    many = client.webhooks().list()
    assert isinstance(many, list)
