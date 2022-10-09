import json

from flask import render_template, Response, g
from flask_sqlalchemy import Pagination
from htmlmin.minify import html_minify

from ProdManager.helpers.json import json_defaults

def custom_render_template(*args, **kwargs):
  response = None

  if 'json' in kwargs and g.api:
    resources = kwargs['json']['resources']
    serialize = kwargs['json'].get('serialize', True)

    if isinstance(resources, Pagination):
      if serialize:
        data = dict(items=[resource.api_serialize for resource in resources.items])
      else:
        data = resources.items

      response = Response(
        response=json.dumps(
          data,
          sort_keys=True, default=json_defaults
        ),
        content_type="application/json",
        headers=[
          ('x-total-pages', resources.pages),
          ('x-total', resources.total),
          ('x-page', resources.page),
          ('x-per-page', resources.per_page),
          ('x-prev-page', resources.prev_num),
          ('x-next-page', resources.next_num),
        ]
      )
    else:
      if serialize:
        data = resources.api_serialize
      else:
        data = resources

      response = Response(
        response=json.dumps(data, sort_keys=True, default=json_defaults),
        content_type="application/json",
      )
  else:
    rendered_html = render_template(*args, **kwargs)
    response = html_minify(rendered_html, ignore_comments=False, parser="lxml")

  return response
