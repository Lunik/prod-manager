from pkg_resources import parse_version
import pytest

import responses

from ProdManager import create_app
from ProdManager import __version__
from ProdManager.helpers.hello import Hello

HELLO_ENDPOINT = "https://hello.prod-manager.tiwabbit.fr"

app = create_app()

def test_hello():
  app.config["DISABLE_HELLO"] = True
  hello = Hello(app)

  app.config["DISABLE_HELLO"] = False
  hello = Hello(app)

def test_playload():
  playload = Hello.generate_playload(app)

  assert playload["version"] == __version__

@responses.activate
def test_post_playload():
  responses.get(HELLO_ENDPOINT, status=200, json={ "message": "olleH" })

  hello = Hello(app)
  playload = Hello.hello(hello, app)
