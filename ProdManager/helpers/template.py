
from flask import render_template
from htmlmin.minify import html_minify

def custom_render_template(*args, **kwargs):
  rendered_html = render_template(*args, **kwargs)
  return html_minify(rendered_html, ignore_comments=False)
