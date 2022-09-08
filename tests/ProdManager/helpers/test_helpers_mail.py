
from unittest import mock, TestCase
from unittest.mock import MagicMock

from ProdManager.helpers.mail import (
  MailWorker,
)

class App:
  def __init__(self):
    self.config = dict(
      MAIL_ENABLED=True,
      MAIL_SERVER="localhost",
      MAIL_PORT=587,
      MAIL_USERNAME="unittest",
      MAIL_PASSWORD="unittest",
      MAIL_USE_SSL=False,
      MAIL_USE_TLS=True,
      MAIL_VALIDATE_CERTS=True,
      MAIL_USE_CREDENTIALS=True,
      MAIL_SENDER="unittest@localhost.local",
      MAIL_PREFIX="[UNITTEST]",
      MAIL_REPLY_TO="unittest@localhost.local",
    )


def test_init_app():
  mail = MailWorker()

  app = App()

  mail.init_app(app)

  app.config["MAIL_USE_SSL"] = True
  app.config["MAIL_USE_TLS"] = True
  with TestCase().assertRaises(Exception):
    mail.init_app(app)

@mock.patch('smtplib.SMTP')
def test_connect(mock_SMTP):
  mock_SMTP_instance = mock_SMTP.return_value

  mail = MailWorker()

  app = App()
  mail.init_app(app)

  mail.connect()

  mock_SMTP_instance.starttls.assert_called_once()
  mock_SMTP_instance.login.assert_called_once()

@mock.patch('smtplib.SMTP_SSL')
def test_connect_2(mock_SMTP):
  mock_SMTP_instance = mock_SMTP.return_value

  mail = MailWorker()

  app = App()
  app.config["MAIL_USE_SSL"] = True
  app.config["MAIL_USE_TLS"] = False
  mail.init_app(app)

  mail.connect()

  mock_SMTP_instance.starttls.assert_not_called()
  mock_SMTP_instance.login.assert_called_once()

@mock.patch('smtplib.SMTP')
def test_send_mail(mock_SMTP):
  mock_SMTP_instance = mock_SMTP.return_value

  mail = MailWorker()

  app = App()
  mail.init_app(app)

  worker = mail.send_mail(["unittest@localhost.local"], subject="unitest", body="the body")
  worker.join()

  mock_SMTP_instance.send_message.assert_called_once()

@mock.patch('smtplib.SMTP')
def test_send_mail_2(mock_SMTP):
  mock_SMTP_instance = mock_SMTP.return_value

  mail = MailWorker()

  app = App()
  mail.init_app(app)
  mail.enabled = False

  worker = mail.send_mail(["unittest@localhost.local"], subject="unitest", body="the body")
  assert worker is None

  mock_SMTP_instance.send_message.assert_not_called()

@mock.patch('smtplib.SMTP')
def test_send_mail_3(mock_SMTP):
  mock_SMTP_instance = mock_SMTP.return_value

  mail = MailWorker()

  app = App()
  mail.init_app(app)

  worker = mail.send_mail([], subject="unitest", body="the body")
  assert worker is None

  mock_SMTP_instance.send_message.assert_not_called()