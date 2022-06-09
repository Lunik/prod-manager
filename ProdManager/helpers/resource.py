from flask import current_app
from sqlalchemy.exc import IntegrityError
from ProdManager import db
from ProdManager.helpers.response import (
  NotFoundError, ServerError, ConflictError,
  UndeletableRessourceError, DependencyError,
)

def list_resources(ressource_class):
  # https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.BaseQuery.paginate
  # page, per_page and max_per_page are retreived from the Flask.request object
  return ressource_class.query.order_by(
    ressource_class.id.asc()
  ).paginate(error_out=False)

def list_resources_as_choices(ressource_class):
  return [
    (resource.id, resource.name) for resource in
    ressource_class.query.order_by(ressource_class.id.asc())
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
    raise error

  return resource
