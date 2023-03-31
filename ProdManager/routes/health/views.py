
from flask import Blueprint, current_app

bp = Blueprint("health", __name__)

@bp.route("", methods=("GET",))
def probe():
  return "OK", 200

@bp.route('/version')
def version():
  return current_app.version.serialize, 200
