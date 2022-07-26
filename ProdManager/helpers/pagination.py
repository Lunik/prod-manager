from flask import request

from .links import custom_url_for


def url_for_paginated(endpoint, page, per_page):

  kwargs = request.args.copy()

  kwargs["page"] = page
  kwargs["per_page"] = per_page

  return custom_url_for(endpoint, **kwargs)
