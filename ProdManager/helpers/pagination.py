from flask import request, abort

from ProdManager import lang

from .links import custom_url_for

def url_for_paginated(endpoint, page, per_page):

  kwargs = request.args.copy()

  kwargs["page"] = page
  kwargs["per_page"] = per_page

  return custom_url_for(endpoint, **kwargs)

PAGINATION_MAX_PAGE = 10000000
PAGINATION_MAX_PER_PAGE = 50

def secure_pagination():
  reasons = dict()

  page = request.args.get('page')
  if page and int(page) > PAGINATION_MAX_PAGE:
    reasons['page'] = [f"Value higher than the limit {PAGINATION_MAX_PAGE}"]

  per_page = request.args.get('per_page')
  if per_page and int(per_page) > PAGINATION_MAX_PER_PAGE:
    reasons['per_page'] = [f"Value higher than the limit {PAGINATION_MAX_PER_PAGE}"]

  if len(reasons):
    abort(400, dict(
      message=lang.get("pagination_overflow"),
      reasons=reasons
    ))
