import functools
import logging
from sqlite3 import IntegrityError as sqlite3IntegrityError

from flask import current_app, request
from sqlalchemy.exc import IntegrityError

from psycopg2.errors import (
  UniqueViolation as pgsqlUniqueViolation,
  NotNullViolation as pgsqlNotNullViolation,
)

from ProdManager import db
from ProdManager.models import EventType
import ProdManager.helpers.notification as NotificationHelper
import ProdManager.helpers.event as EventHelper
from .response import (
  NotFoundError, ServerError, ConflictError,
  UndeletableRessourceError, DependencyError,
)

logger = logging.getLogger('gunicorn.error')


def list_resources_from_query(ressource_class, query, orders=None, filters=None, paginate=True, limit=50):
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

  for attribute, new_value in attributs.items():
    old_value = getattr(resource, attribute)

    if old_value != new_value:
      setattr(resource, attribute, new_value)
      changed[attribute] = (old_value, new_value)

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
    NotificationHelper.notify(NotificationHelper.NotificationType.UPDATE, resource_class, resource)
    EventHelper.create_event(EventType.UPDATE, resource_class, resource, changed)

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

  NotificationHelper.notify(NotificationHelper.NotificationType.CREATE, resource_class, resource)
  EventHelper.create_event(EventType.CREATE, resource_class, resource)

  logger.info(f"Created {resource}")

  return resource

def resource_filters(filter_fields):
  def decorate(view):

    @functools.wraps(view)
    def wrapped_view(**kwargs):
      filters = ()

      for filter_name, filter_field, filter_type, filter_operator in filter_fields:
        filter_value = request.args.get(filter_name, type=filter_type)
        if filter_value is not None:
          match filter_operator:
            case 'gt':
              filters += (filter_field > filter_value,)
            case 'ge':
              filters += (filter_field >= filter_value,)
            case 'lt':
              filters += (filter_field < filter_value,)
            case 'le':
              filters += (filter_field < filter_value,)
            case 'ne':
              filters += (filter_field != filter_value,)
            case _:
              filters += (filter_field == filter_value,)

      kwargs['filters'] = filters
      return view(**kwargs)

    return wrapped_view

  return decorate
