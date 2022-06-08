import enum

class ModelEnum(enum.Enum):
  @classmethod
  def choices(cls):
    return [(choice.value, choice.name) for choice in cls]

  @classmethod
  def coerce(cls, item):
    item = cls(item) if not isinstance(item, cls) else item
    return item.value

  def __gt__(self, other):
    if isinstance(other, ModelEnum):
      return (
        self._member_names_.index(self.name) >
        self._member_names_.index(other.name)
      )
    return NotImplemented
