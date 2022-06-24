
from ProdManager import mail

from ProdManager.models.Subscriber import Subscriber
from ProdManager.helpers.resource import list_resources

def send_notification(title, content):
  return mail.send_mail(
    [subscriber.email for subscriber in list_resources(Subscriber, paginate=False)],
    title,
    content,
  )
