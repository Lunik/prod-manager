
from flask import Blueprint

bp = Blueprint("health", __name__)

@bp.route("", methods=("GET",))
def probe():
  return "OK", 200
