import json

from flask import current_app

from ProdManager.models import (
  Incident, Maintenance, EventType,
)
import ProdManager.helpers.resource as ResourceHelpers
from ProdManager.helpers.json import json_defaults

from .date import current_date

EVENT_SUPPORTED_RESOURCES = [
  Incident, Maintenance,
]


def create_event(event_type, resource_class, resource, changed=None):
  if not isinstance(event_type, EventType):
    raise Exception("event_type is not of type : EventType")

  if resource_class not in EVENT_SUPPORTED_RESOURCES:
    return

  try:
    data = dict(
      creation_date=current_date(rounded=False),
      type=event_type,
      content=json.dumps(changed or resource.serialize, default=json_defaults),
    )
    data[f"{resource_class.__name__.lower()}_id"] = resource.id

    _ = ResourceHelpers.create_resource(resource_class.event_type, data)
  except Exception as error:
    current_app.logger.error(
      f"Unable to create event during {resource_class.__name__} creation : {error}"
    )
