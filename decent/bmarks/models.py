from django.db import models
from django.contrib.auth.models import User

optional = dict(blank=True, null=True)

class Address(models.Model):
    username = models.CharField(max_length=30)
    domain = models.URLField()
    
class Human(User):
    # username
    # email
    # password
    address = models.OneToOneField(Address)
    
class Subscription(Address):
    the_person_listening = models.ForeignKey(Human)
    last_received_update = models.DateTimeField()

class Subscriber(Address):
    the_person_sending = models.ForeignKey(Human)
    last_updated = models.DateTimeField()
    
class Tag(models.Model):
    name = models.CharField(max_length=30)
    
class Bookmark(models.Model):
    owner = models.ForeignKey(Human)
    url = models.URLField()
    description = models.TextField(**optional)
    tags = models.ManyToManyField(Tag, **optional)
    time = models.DateTimeField(auto_now_add=True)  # auto on create
    # via (a given address)
    # is_private
