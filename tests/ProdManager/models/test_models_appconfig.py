from uuid import UUID

from ProdManager import create_app

from ProdManager.models.AppConfig import AppConfig

app = create_app()

def test_app_config():
  with app.app_context():
    count = AppConfig.query.count()

    assert count == 1

def test_app_config_uuid():
  with app.app_context():
    app_config = AppConfig.query.first()

    assert UUID(app_config.uuid)

    assert app_config.uuid == app_config.serialize["uuid"]
    assert app_config.uuid == app_config.api_serialize["uuid"]
