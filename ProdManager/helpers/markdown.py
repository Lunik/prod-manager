from flask import Markup
from markupsafe import escape
from jinja2 import pass_eval_context
import markdown as md

class Markdown:
  def __init__(self, app=None, auto_escape=False, **markdown_options):
    self.auto_escape = auto_escape
    self._instance = md.Markdown(**markdown_options)
    if app:
      self.init_app(app)

  def init_app(self, app):
    app.jinja_env.filters.setdefault(
      'markdown', self.__build_filter(self.auto_escape))

  def __call__(self, stream):
    return Markup(self._instance.convert(stream))

  def __build_filter(self, app_auto_escape):
    @pass_eval_context
    def markdown_filter(eval_ctx, stream):
      __filter = self
      if app_auto_escape and eval_ctx.autoescape:
        return Markup(__filter(escape(stream)))

      return Markup(__filter(stream))

    return markdown_filter
