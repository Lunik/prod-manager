from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_redis import FlaskRedis

from ProdManager.helpers.mail import MailWorker
from ProdManager.helpers.lang import LangManager
from ProdManager.helpers.markdown import Markdown

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
redis_client = FlaskRedis()
mail = MailWorker()
lang = LangManager()
markdown = Markdown(
  extensions=[
    'markdown.extensions.tables',
    'markdown.extensions.sane_lists',
    'markdown.extensions.nl2br',
    'markdown.extensions.fenced_code',
    'markdown.extensions.codehilite'
  ]
)
