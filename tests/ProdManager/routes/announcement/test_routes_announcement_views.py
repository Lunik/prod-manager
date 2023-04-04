import random
import string
import re
from datetime import datetime

import flask_unittest
import flask.globals
from flask import request

from ProdManager import create_app

class TestRoutesAnnouncementViews(flask_unittest.AppTestCase):

  def create_app(self):
    app = create_app(scheduled_jobs=False)
    app.config['WTF_CSRF_ENABLED'] = False
    return app


  def test_list_endpoint_with_app(self, app):
    with app.test_request_context('/announcement'):
      self.assertEqual(request.endpoint, 'announcement.list')

  def test_show_endpoint_with_app(self, app):
    with app.test_request_context('/announcement/1'):
      self.assertEqual(request.endpoint, 'announcement.show')

  def test_list_with_client(self, app):
    with app.test_client() as client:
      rv = client.get('/announcement')
      self.assertInResponse(b'<h1>Announcements list</h1>', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_create_with_client(self, app):
    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/announcement/create', data=dict(
        scope="1",
        service="1",
        level="high",
        start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        description="placeholder"
      ))
      assert re.match(r"http://localhost/announcement/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/announcement/create', data=dict(
        service="1",
        level="high",
        start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        description="placeholder"
      ))
      assert b"scope : This field is required" in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

    with app.test_client() as client:
      rv = client.post('/announcement/create', data=dict(
        service="1",
        level="high",
        start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}",
        description="placeholder"
      ))
      assert rv.status_code == 403
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_show_with_client(self, app):
    announcement_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/announcement/create', data=dict(
        scope="1",
        service="1",
        level="high",
        start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=announcement_name,
        description="placeholder"
      ))

      rv = client.get(rv.headers.get('Location'))

      self.assertInResponse(f'<h1 id="title">Announcement - {announcement_name}</h1>'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get("/announcement/-1")

      assert rv.status_code == 404
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_update_with_client(self, app):
    announcement_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"
    announcement_name_2 = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/announcement/create', data=dict(
        scope="1",
        service="1",
        level="medium",
        start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=announcement_name,
        description="placeholder"
      ))

      announcement_uri = rv.headers.get('Location')

      rv = client.post(f"{announcement_uri}/update", data=dict(
        scope="1",
        service="1",
        level="medium",
        start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=announcement_name_2,
        description="placeholder"
      ))

      assert re.match(r"http://localhost/announcement/\d+", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.get(announcement_uri)

      self.assertInResponse(f'<h1 id="title">Announcement - {announcement_name_2}</h1>'.encode(), rv)
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{announcement_uri}/update", data=dict(
        scope="1",
        service="1",
        start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=announcement_name_2,
        description="placeholder"
      ))

      assert b"level : This field is required" in rv.data
      assert rv.status_code == 400
      self.assertNotIn(b"__missing_translation", rv.data)

      rv = client.post(f"{announcement_uri}/update", data=dict(
        scope="1",
        service="1",
        level="low",
        start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=announcement_name_2,
        description="placeholder"
      ))

      rv = client.get(announcement_uri)

      self.assertInResponse(b'LOW', rv)
      self.assertNotIn(b"__missing_translation", rv.data)

  def test_delete_with_client(self, app):
    announcement_name = f"TEST-{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    with app.test_client() as client:
      client.post('/login', data=dict(secret="changeit"))
      rv = client.post('/announcement/create', data=dict(
        scope="1",
        service="1",
        level="low",
        start_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        end_date=datetime.now().strftime('%Y-%m-%dT%H:%M'),
        name=announcement_name,
        description="placeholder"
      ))

      announcement_uri = rv.headers.get('Location')

      rv = client.post(f"{announcement_uri}/delete")

      assert re.match(r"http://localhost/announcement", rv.headers.get('Location'))
      assert rv.status_code == 302
      self.assertNotIn(b"__missing_translation", rv.data)


      rv = client.post(f"/announcement/-1/delete")

      assert rv.status_code == 404
      self.assertNotIn(b"__missing_translation", rv.data)
