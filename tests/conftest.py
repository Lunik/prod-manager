import pytest
import socket

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

@pytest.helpers.register
def redis_available(hostname, port):
  try:
    socket.gethostbyname_ex(hostname)
  except Exception as error:
    return False

  return socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect_ex((hostname, port)) == 0