from django.db import models
from django.contrib.auth.models import User

optional = dict(blank=True, null=True)

class Address(models.Model):
    username = models.CharField(max_length=20)
    domain = models.CharField(max_length=50, default="localhost")
    
    def __unicode__(self):
        return self.username + '@' + self.domain
        
    
class Human(User):
    # username
    # password
    # email
    address = models.OneToOneField(Address)
    
    
class Subscription(Address):
    the_person_listening = models.ForeignKey(Human)
    last_received_update = models.DateTimeField()
    
    def __unicode__(self):
        return 'From: ' + self.the_person_listening + 'to: ' + self.username + '@' + self.domain
        

class Subscriber(Address):
    the_person_sending = models.ForeignKey(Human)
    last_updated = models.DateTimeField()
    
    def __unicode__(self):
        return 'From: ' + self.the_person_sending + 'to: ' + self.username + '@' + self.domain
        
    
class Tag(models.Model):
    name = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.name
    
    
class Bookmark(models.Model):
    owner = models.ForeignKey(Address)
    url = models.URLField()
    description = models.TextField(**optional)
    tags = models.ManyToManyField(Tag, **optional)
    time = models.DateTimeField(auto_now_add=True)  # auto on create
    # via (a given address)
    # is_private
    
    def __unicode__(self):
        return self.url
        
    class Meta:
        ordering = ['-time', 'owner']
