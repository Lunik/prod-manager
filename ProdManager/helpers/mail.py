import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging

from threading import Thread


class MailWorker():
  logger = logging.getLogger('gunicorn.error')
  enabled = False
  server = None
  port = 587
  username = None
  password = None
  use_ssl = False
  use_tls = True
  validate_certs = True
  use_credentials = True
  sender = None
  mail_prefix = "[ProdManager]"
  reply_to = None

  def init_app(self, flask_app):
    self.enabled = flask_app.config["MAIL_ENABLED"]

    if not self.enabled:
      return

    self.server = flask_app.config["MAIL_SERVER"]
    self.port = flask_app.config["MAIL_PORT"]
    self.username = flask_app.config["MAIL_USERNAME"]
    self.password = flask_app.config["MAIL_PASSWORD"]
    self.use_ssl = flask_app.config["MAIL_USE_SSL"]
    self.use_tls = flask_app.config["MAIL_USE_TLS"]
    self.validate_certs = flask_app.config["MAIL_VALIDATE_CERTS"]
    self.use_credentials = flask_app.config["MAIL_USE_CREDENTIALS"]
    self.sender = flask_app.config["MAIL_SENDER"]
    self.mail_prefix = flask_app.config["MAIL_PREFIX"]
    self.reply_to = flask_app.config["MAIL_REPLY_TO"]

    if self.use_ssl and self.use_tls:
      raise Exception("SSL and TLS cannot be enabled together when configuring email notifications")

    if self.validate_certs:
      context = ssl.create_default_context()
    else:
      context = ssl._create_unverified_context()

    if self.use_ssl:
      self.server = smtplib.SMTP_SSL(self.server, self.port, context=context)
    else:
      self.server = smtplib.SMTP(self.server, self.port)

    if self.use_tls:
      self.server.starttls(context=context)

    if self.use_credentials:
      self.server.login(self.username, self.password)

    flask_app.mail = self


  @staticmethod
  def send_async_email(mail, message):
    mail.logger.info("Mail sent")
    mail.server.send_message(message, message["From"])


  def send_mail(self, to_emails, subject, body):
    if not self.enabled:
      return None

    if len(to_emails) == 0:
      return None

    message = MIMEMultipart("alternative")

    message["Subject"] = f"{self.mail_prefix} {subject}"
    message["From"] = self.sender
    message["Bcc"] = ",".join(to_emails)
    if self.reply_to:
      message["Reply-To"] = self.reply_to

    message.attach(MIMEText(body, "html"))

    worker = Thread(target=self.send_async_email, args=[self, message])
    worker.start()

    return worker
