
from ProdManager.helpers.lang import LangManager
from ProdManager import create_app

def test_lang_manager():
  app = create_app(scheduled_jobs=False)

  lang = LangManager()

  lang.init_app(app)

  assert lang.get("dashboard_title") == "Dashboard"
  assert lang.get("undefined_text") == "__missing_translation_undefined_text"

def test_lang_manager_2():
  app = create_app(scheduled_jobs=False)

  app.config["LANG"] = "fr"

  lang = LangManager()

  lang.init_app(app)

  assert lang.get("dashboard_title") == "Tableau de bord"

def test_lang_manager_3():
  app = create_app(scheduled_jobs=False)

  app.config["LANG"] = "xxxx"

  lang = LangManager()

  lang.init_app(app)

  assert lang.get("dashboard_title") == "Dashboard"