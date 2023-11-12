from .models import *

def get_ticket_item():
  if Item.objects.filter(name="message ticket").count() > 0:
    return Item.objects.filter(name="message ticket").first()
  Item.objects.create(
    name="message ticket",
    description="message ticket",
    cost=1,
    category='renewable')
  return Item.objects.filter(name="message ticket").first()

def get_num_tickets(user : Account):
  item = get_ticket_item()
  return Purchase.objects.filter(item=item, user=user).count()

def eat_ticket(user : Account):
  if (get_num_tickets(user) == 0):
    return False
  Purchase.objects.filter(item=get_ticket_item(), user=user).first().delete()
  return True