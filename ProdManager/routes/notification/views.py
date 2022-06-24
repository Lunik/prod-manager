
from flask import Blueprint, render_template, abort, redirect, url_for
from sqlalchemy.exc import NoResultFound

from ProdManager.models.Subscriber import Subscriber

from ProdManager.helpers.resource import create_resource, list_resources, delete_resource
from ProdManager.helpers.response import ConflictError

from .forms import SubscribeForm, UnSubscribeForm

bp = Blueprint("notification", __name__, url_prefix="/")


@bp.route('', methods=("GET",))
def index():
  return render_template("notification/page.html",
    subscribe_form=SubscribeForm(),
    unsubscribe_form=UnSubscribeForm(),
  ), 200

@bp.route('/suscribe', methods=("POST",))
def subscribe():
  form=SubscribeForm()

  if not form.validate_on_submit():
    abort(400, dict(
      message="Notification subscription failed",
      reasons=form.errors
    ))

  try:
    _ = create_resource(Subscriber, dict(
      email=form.email.data,
    ))
  except ConflictError:
    pass
  except Exception as error:
    return abort(error.code, dict(
      message="Notification subscription failed",
      reasons=dict(scope=error.message)
    ))

  return redirect(url_for('notification.index', info_message="Successfully subscribed"), 302)

@bp.route('/unsuscribe', methods=("POST",))
def unsubscribe():
  form=SubscribeForm()

  if not form.validate_on_submit():
    abort(400, dict(
      message="Notification unsubscription failed",
      reasons=form.errors
    ))

  try:
    subscriber = list_resources(
      Subscriber,
      filters=(Subscriber.email == form.email.data,),
      paginate=False
    ).one()
  except NoResultFound:
    subscriber = None
  except Exception as error:
    return abort(error.code, dict(
      message="Notification subscription failed",
      reasons=dict(scope=error.message)
    ))

  if subscriber:
    try:
      delete_resource(Subscriber, subscriber.id)
    except Exception as error:
      return abort(error.code, dict(
        message="Notification unsubscription failed",
        reasons=dict(scope=error.message)
      ))

  return redirect(url_for('notification.index', info_message="Successfully unsubscribed"), 302)
