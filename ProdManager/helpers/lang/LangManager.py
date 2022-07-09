import logging
import pathlib
import yaml

from ProdManager.helpers.yaml import myloader


class LangManager():
  logger = logging.getLogger('gunicorn.error')

  default = "en"
  current = None
  supported = ["en", "fr"]

  _translations = None
  _default_translations = None

  def init_app(self, flask_app):
    flask_app.lang = self

    if flask_app.config["LANG"] in self.supported:
      self.current = flask_app.config["LANG"]
    else:
      self.current = self.default

    self._load()

  def _load(self):
    with open(
      f"{pathlib.Path(__file__).parent.resolve()}/translations/{self.current}.yml",
      'r',
      encoding="UTF-8"
    ) as file:
      self._translations = yaml.load(file, Loader=myloader)

    if self.current != self.default:
      with open(
        f"{pathlib.Path(__file__).parent.resolve()}/translations/{self.default}.yml",
        'r',
        encoding="UTF-8"
      ) as file:
        self._default_translations = yaml.load(file, Loader=myloader)
    else:
      self._default_translations = self._translations

  def get(self, message_id):
    return self._translations.get(message_id) \
      or self._default_translations.get(message_id, f"__missing_translation_{message_id}")
