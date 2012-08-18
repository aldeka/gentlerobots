from django.db import models
from django.auth.models import User

# add **optional

class Address(models.Model):
    username = models.CharField(max_length=30)
    domain = models.URLField()
    
class Human(User):
    address = models.ForeignKey(Address)
    
class Subscription(Address):
    the_person_listening = models.ForeignKey(Human)
    last_received_update = models.DateTimeField()  # todo, make this default on create

class Subscriber(Address):
    the_person_sending = models.ForeignKey(Human)
    last_updated = models.DateTimeField()  # todo, make this default on create
    
class Tag(models.Model):
    name = models.CharField(max_length=30)
    
class Bookmark(models.Model):
    owner = models.ForeignKey(Human)
    url = models.URLField()
    description = models.TextField(**optional)
    tags = models.ManytoManyField(Tag, **optional)
    date = models.DateTimeField()  # auto on create
    # via (a given address)
    # is_private
