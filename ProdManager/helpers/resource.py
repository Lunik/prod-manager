import functools
import logging
from sqlite3 import IntegrityError as sqlite3IntegrityError

from flask import current_app, request, abort
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from psycopg2.errors import (
  UniqueViolation as pgsqlUniqueViolation,
  NotNullViolation as pgsqlNotNullViolation,
)

from ProdManager.plugins import db, lang
from ProdManager.models import EventType
import ProdManager.helpers.notification as NotificationHelper
import ProdManager.helpers.event as EventHelper
from .response import (
  NotFoundError, ServerError, ConflictError,
  UndeletableRessourceError, DependencyError,
)
from .pagination import PAGINATION_MAX_PER_PAGE

logger = logging.getLogger('gunicorn.error')


def list_resources_from_query(ressource_class, query, orders=None, filters=None, paginate=True, limit=PAGINATION_MAX_PER_PAGE):
  if orders is None:
    orders = ressource_class.default_order()

  if not isinstance(orders, tuple):
    orders = (orders,)

  if filters is not None:
    if not isinstance(filters, tuple):
      filters = (filters,)

    query = query.filter(*filters)

  result = query.order_by(*orders)

  if not paginate and limit:
    result = result.limit(limit)

  # https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.BaseQuery.paginate
  # page, per_page and max_per_page are retreived from the Flask.request object
  if paginate:
    result = result.paginate(error_out=False, max_per_page=limit)

  return result

def list_resources(ressource_class, *args, **kwargs):
  return list_resources_from_query(ressource_class, ressource_class.query, *args, **kwargs)


def list_resources_as_choices(ressource_class, order=None):
  if order is None:
    order = ressource_class.id.asc()

  return [
    (resource.id, resource.name) for resource in
    ressource_class.query.order_by(order)
  ]

def get_resource(resource_class, ressource_id):
  resource = resource_class.query.get(ressource_id)

  if resource is None:
    raise NotFoundError(ressource_id)

  return resource


def update_resource(resource_class, ressource_id, attributs):
  resource = resource_class.query.get(ressource_id)

  if resource is None:
    raise NotFoundError(ressource_id)

  changed = {}
  should_notify = False

  for attribute, new_value in attributs.items():
    old_value = getattr(resource, attribute)

    if old_value != new_value:
      setattr(resource, attribute, new_value)
      changed[attribute] = (old_value, new_value)

      if hasattr(resource_class, 'notify_attributs') \
        and (attribute in resource_class.notify_attributs):
        should_notify = True

  try:
    db.session.commit()

  except IntegrityError as error:
    db.session.rollback()
    if isinstance(error.orig, pgsqlUniqueViolation) \
      or (isinstance(error.orig, sqlite3IntegrityError) and "UNIQUE constraint failed" in str(error)):
      raise ConflictError(attributs) from error

    raise ServerError(error) from error

  except Exception as error:
    current_app.logger.error(error)
    raise error

  if len(changed.keys()) > 0:
    EventHelper.create_event(EventType.UPDATE, resource_class, resource, changed)

    if should_notify:
      NotificationHelper.notify(
        NotificationHelper.NotificationType.UPDATE,
        resource_class,
        resource
      )

  logger.info(f"Updated {resource}")

  return resource, changed


def delete_resource(resource_class, ressource_id):
  resource = resource_class.query.get(ressource_id)

  if resource is None:
    raise NotFoundError(ressource_id)

  if hasattr(resource, "default") and resource.default:
    raise UndeletableRessourceError("This is a default resource")

  db.session.delete(resource)

  try:
    db.session.commit()
  except IntegrityError as error:
    db.session.rollback()
    if isinstance(error.orig, pgsqlNotNullViolation) \
      or (isinstance(error.orig, sqlite3IntegrityError) and "NOT NULL constraint failed" in str(error)):
      raise DependencyError("This resource is a dependency from other resources") from error

    raise ServerError(error) from error

  except Exception as error:
    current_app.logger.error(error)
    raise ServerError(error) from error

  logger.info(f"Deleted {resource}")


def create_resource(resource_class, attributs):
  resource = resource_class(**attributs)

  db.session.add(resource)

  try:
    db.session.commit()

  except IntegrityError as error:
    db.session.rollback()
    if isinstance(error.orig, pgsqlUniqueViolation) \
      or (isinstance(error.orig, sqlite3IntegrityError) and "UNIQUE constraint failed" in str(error)):
      raise ConflictError(attributs) from error

    raise ServerError(error) from error

  except Exception as error:
    current_app.logger.error(error)
    raise ServerError(error) from error

  EventHelper.create_event(EventType.CREATE, resource_class, resource)

  NotificationHelper.notify(
    NotificationHelper.NotificationType.CREATE,
    resource_class,
    resource
  )

  logger.info(f"Created {resource}")

  return resource

def resource_filters(filter_fields):
  def decorate(view):

    @functools.wraps(view)
    def wrapped_view(**kwargs):
      filters = ()

      for filter_name in request.args:
        if filter_name not in filter_fields:
          continue

        filter_field, filter_type, filter_operator = filter_fields[filter_name]

        filter_values = request.args.getlist(filter_name, type=filter_type)
        filter_values_count = len(filter_values)
        if filter_values_count == 0:
          continue

        if filter_values_count > PAGINATION_MAX_PER_PAGE:
          abort(400, dict(
            message=lang.get("filter_overflow"),
            reasons=dict(filter_name=[f"Filter occurrence count higher than the limit {PAGINATION_MAX_PER_PAGE}"])
          ))

        current_filter = []

        for filter_value in filter_values:
          match filter_operator:
            case 'gt':
              current_filter.append(filter_field > filter_value)
            case 'ge':
              current_filter.append(filter_field >= filter_value)
            case 'lt':
              current_filter.append(filter_field < filter_value)
            case 'le':
              current_filter.append(filter_field < filter_value)
            case 'ne':
              current_filter.append(filter_field != filter_value)
            case _:
              current_filter.append(filter_field == filter_value)

        filters += (or_(*current_filter),)

      kwargs['filters'] = filters
      return view(**kwargs)

    return wrapped_view

  return decorate
