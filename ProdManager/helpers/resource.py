from flask import current_app
from sqlalchemy.exc import IntegrityError
from ProdManager import db
from ProdManager.helpers.response import (
  NotFoundError, ServerError, ConflictError,
  UndeletableRessourceError, DependencyError,
)

def list_resources_from_query(ressource_class, query, orders=None, filters=None, paginate=True):
  if orders is None:
    orders = ressource_class.default_order()

  if not isinstance(orders, tuple):
    orders = (orders,)

  if filters is not None:
    if not isinstance(filters, tuple):
      filters = (filters,)

    query = query.filter(*filters)

  result = query.order_by(*orders)

  # https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.BaseQuery.paginate
  # page, per_page and max_per_page are retreived from the Flask.request object
  if paginate:
    result = result.paginate(error_out=False)

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
    if "UNIQUE constraint failed" in str(error):
      raise ConflictError(attributs) from error

    raise ServerError(error) from error

  except Exception as error:
    current_app.logger.error(error)
    raise error

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
    if "NOT NULL constraint failed" in str(error):
      raise DependencyError("This resource is a dependency from other resources") from error

    raise ServerError(error) from error

  except Exception as error:
    current_app.logger.error(error)
    raise ServerError(error) from error


def create_resource(resource_class, attributs):
  resource = resource_class(**attributs)

  db.session.add(resource)

  try:
    db.session.commit()

  except IntegrityError as error:
    db.session.rollback()
    if "UNIQUE constraint failed" in str(error):
      raise ConflictError(attributs) from error

    raise ServerError(error) from error

  except Exception as error:
    current_app.logger.error(error)
    raise ServerError(error) from error

  return resource
