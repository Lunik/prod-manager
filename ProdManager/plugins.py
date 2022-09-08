from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from ProdManager.helpers.mail import MailWorker
from ProdManager.helpers.lang import LangManager

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
mail = MailWorker()
lang = LangManager()
