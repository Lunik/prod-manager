
import pytest
import random
import string

from flask_sqlalchemy import Pagination, BaseQuery

from ProdManager.helpers.resource import (
  list_resources_from_query, list_resources,
  list_resources_as_choices, get_resource,
  update_resource, delete_resource,
  create_resource, resource_filters,
)

from ProdManager.helpers.response import ( 
  NotFoundError, ServerError, ConflictError, 
  UndeletableRessourceError, DependencyError, 
) 

from ProdManager import create_app

from ProdManager.models import (
  Scope, Service, Incident,
  Monitor,
)

app = create_app()

def test_list_resources():
  with app.app_context():
    resources = list_resources(Scope)

    assert resources.total > 0
    assert isinstance(resources, Pagination)
    assert isinstance(resources.items[0], Scope)

    resources = list_resources(Scope, paginate=False)

    assert resources.count() > 0
    assert isinstance(resources, BaseQuery)
    assert isinstance(resources.first(), Scope)

def test_list_resources_as_choices():
  with app.app_context():
    resources = list_resources_as_choices(Scope)

    assert len(resources) > 0

def test_get_resource():
  with app.app_context():
    resource = get_resource(Scope, 1)

    assert isinstance(resource, Scope)

  with app.app_context():
    with pytest.raises(NotFoundError):
      resource = get_resource(Scope, -1)

def test_update_resource():
  with app.app_context():
    name_old = f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
    name_new = f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
    resource = create_resource(Scope, dict(name=name_old))

    resource, changed = update_resource(Scope, resource.id, dict(name=name_new))

    assert isinstance(resource, Scope)
    assert resource.name == name_new
    assert "name" in changed
    assert changed['name'] == (name_old, name_new)

  with app.app_context():
    with pytest.raises(NotFoundError):
      resource, changed = update_resource(Scope, -1, dict())

  with app.app_context():
    name_1 = f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
    name_2 = f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
    resource_1 = create_resource(Scope, dict(name=name_1))
    resource_2 = create_resource(Scope, dict(name=name_2))

    with pytest.raises(ConflictError):
      resource, changed = update_resource(Scope, resource_2.id, dict(name=name_1))

def test_create_resource():
  with app.app_context():
    resource = create_resource(Scope, dict(name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"))

    assert isinstance(resource, Scope)

  with app.app_context():
    with pytest.raises(ConflictError):
      resource = create_resource(Scope, dict(name=f"UNIT_TESTS"))
      resource = create_resource(Scope, dict(name=f"UNIT_TESTS"))

def test_delete_resource():
  with app.app_context():
    resource = create_resource(Scope, dict(name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"))

    assert isinstance(resource, Scope)

    delete_resource(Scope, resource.id)

  with app.app_context():
    with pytest.raises(NotFoundError):
      delete_resource(Scope, -1)

  with app.app_context():
    scope_resource = create_resource(Scope, dict(name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"))
    service_resource = create_resource(Service, dict(name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"))
    monitor_resource = create_resource(Monitor, dict(
      name=f"UNIT_TESTS-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
      scope_id=scope_resource.id,
      service_id=service_resource.id
    ))

    with pytest.raises(DependencyError):
      delete_resource(Scope, scope_resource.id)
