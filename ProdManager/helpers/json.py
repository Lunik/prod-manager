from enum import Enum
from datetime import datetime

from .date import beautifull_date

def json_defaults(obj):
  if isinstance(obj, datetime):
    return beautifull_date(obj)

  if isinstance(obj, Enum):
    return obj.name

  raise Exception(f"Json default not implemented for {obj.__class__.__name__}")
