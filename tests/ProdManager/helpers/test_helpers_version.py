from pkg_resources import parse_version
import pytest

import responses

from ProdManager import __version__
from ProdManager.helpers.version import AppVersion

LATEST_VERSION_URL = "https://prodmanager.gitlab.example.org/api/v4/projects/42/releases/permalink/latest"

def test_version():
  version = AppVersion(__version__, LATEST_VERSION_URL)

  assert version.current == parse_version(__version__)

  assert version.is_latest()

def test_version_disabled():
  version = AppVersion(__version__, LATEST_VERSION_URL, disable_check=True)

  assert version.current == parse_version(__version__)

  assert version.is_latest()


def test_version_serialize():
  version = AppVersion(__version__, LATEST_VERSION_URL)

  assert isinstance(version.serialize, dict)


@responses.activate
def test_version_retreive():
  responses.get(LATEST_VERSION_URL, status=200, json={"tag_name": "v0.42.0", "_links": { "self": "https://prodmanager.gitlab.example.org/prod-manager/prod-manager/-/releases/v0.42.0" }})

  version = AppVersion("v0.1.0", LATEST_VERSION_URL)

  AppVersion.retreive_latest(version)

  assert version.latest == parse_version("v0.42.0")
  assert version.release_url == "https://prodmanager.gitlab.example.org/prod-manager/prod-manager/-/releases/v0.42.0"

  assert not version.is_latest()

@responses.activate
def test_version_404():
  responses.get(LATEST_VERSION_URL, status=404, json={"error": "Not Found" })

  version = AppVersion("v0.1.0", LATEST_VERSION_URL)

  AppVersion.retreive_latest(version)

@responses.activate
def test_version_malformated_json():
  responses.get(LATEST_VERSION_URL, status=200, body='not json')

  version = AppVersion("v0.1.0", LATEST_VERSION_URL)

  AppVersion.retreive_latest(version)

@responses.activate
def test_version_missingjson():
  responses.get(LATEST_VERSION_URL, status=200, json={})

  version = AppVersion("v0.1.0", LATEST_VERSION_URL)

  AppVersion.retreive_latest(version)
