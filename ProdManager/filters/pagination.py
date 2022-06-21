from flask import request, url_for


def url_for_paginated(endpoint, page, per_page):

  args = request.args.copy()

  args["page"] = page
  args["per_page"] = per_page

  return url_for(endpoint, **args)
