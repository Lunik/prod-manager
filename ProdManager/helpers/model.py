import enum

class ModelEnum(enum.Enum):
  @classmethod
  def choices(cls):
    return [(choice.value, choice.name) for choice in cls]

  @classmethod
  def coerce(cls, item):
    item = cls(item) if not isinstance(item, cls) else item
    return item.value