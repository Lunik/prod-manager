import pytest

pytest_plugins = ["helpers_namespace"]

@pytest.helpers.register
def generate_token(client, permissions=[]):
  rv = client.post('/api/token/create',
    data=dict(
      secret="changeit",
      name="pytest-unittest",
      description="Token only used for unittests",
      permission=permissions,
  ))

  return rv.data.decode('utf-8').replace('"', '')