
from ProdManager import create_app

from ProdManager.models.Announcement import (
  AnnouncementLevel, Announcement,
)

app = create_app(scheduled_jobs=False)

def test_announcement_title():
  announcement = Announcement(
    name="UNIT-TEST",
    level=AnnouncementLevel.HIGH
  )

  assert "UNIT-TEST" in announcement.title


def test_count_announcements():
  with app.app_context():
    announcement_count = Announcement.count_by_level()

    for level in AnnouncementLevel:
      assert type(announcement_count[level]) == int

  with app.app_context():
    announcement_count = Announcement.count_by_level(serialize=True)

    for level in AnnouncementLevel:
      assert type(announcement_count[level.value]) == int

  with app.app_context():
    announcement_count = Announcement.count_by_level(serialize=True, filters=(Announcement.scope_id == 1,))

    for level in AnnouncementLevel:
      assert type(announcement_count[level.value]) == int
