from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_redis import FlaskRedis

from ProdManager.helpers.mail import MailWorker
from ProdManager.helpers.lang import LangManager

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
redis_client = FlaskRedis()
mail = MailWorker()
lang = LangManager()
