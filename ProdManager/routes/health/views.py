
from flask import Blueprint

bp = Blueprint("health", __name__)

@bp.route("/startup", methods=("GET",))
def startup():
  return "OK", 200

@bp.route("/readiness", methods=("GET",))
def readiness():
  return "OK", 200

@bp.route("/liveness", methods=("GET",))
def liveness():
  return "OK", 200