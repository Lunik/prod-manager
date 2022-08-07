import re

from flask import request, g

api_path_regex = re.compile(r'^/api/.*')

def retreiv_api():
  g.api = api_path_regex.match(request.path) is not None
