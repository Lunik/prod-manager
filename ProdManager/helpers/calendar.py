from datetime import timezone, timedelta
from icalendar import Calendar, Event, Alarm

from ProdManager.filters.links import custom_url_for


class CalendarEvent:

  def __init__(self, start_date, end_date, summary, location, description, categories):
    start_date = start_date.astimezone(timezone.utc)
    end_date = end_date.astimezone(timezone.utc)

    alarm = Alarm()
    alarm.add("trigger", timedelta(minutes=-15))
    alarm.add("action", "display")

    event = Event()
    event.add_component(alarm)
    event.add("dtstart", start_date)
    event.add("dtend", end_date)
    event.add("summary", summary)
    event.add("location", location)
    event.add("description", description)
    event.add("categories", [categories])

    self.cal = Calendar()
    self.cal.add_component(event)

  @classmethod
  def from_maintenance(cls, maintenance):
    summary = maintenance.name
    if maintenance.external_reference:
      summary = f"[{maintenance.external_reference}] {summary}"

    description = f"{maintenance.scope.name}/{maintenance.service.name}"
    if maintenance.description:
      description += f"\n{maintenance.description}"

    return cls(
      start_date=maintenance.scheduled_start_date,
      end_date=maintenance.scheduled_end_date,
      summary=summary,
      location=custom_url_for("maintenance.show", resource_id=maintenance.id),
      description=description,
      categories="Maintenance",
    )

  def render(self):
    return self.cal.to_ical()
