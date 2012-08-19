from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver

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
    
    
class Subscription(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    username = models.CharField(max_length=20)
    domain = models.CharField(max_length=50, default="localhost")
    the_person_listening = models.ForeignKey(Human)
    last_received_update = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return 'From: ' + self.the_person_listening.username + ' to: ' + self.username + '@' + self.domain
        

class Subscriber(models.Model):
    username = models.CharField(max_length=20)
    domain = models.CharField(max_length=50, default="localhost")
    the_person_sending = models.ForeignKey(Human)
    last_updated = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return 'From: ' + self.the_person_sending.username + ' to: ' + self.username + '@' + self.domain
        
    
class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    
    def __unicode__(self):
        return self.name
    
    
class Bookmark(models.Model):
    owner = models.ForeignKey(Address, **optional)
    remote_owner = models.ForeignKey(Subscription, **optional)
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
   
   
### Signals handlers ###

@receiver(post_save, sender=Bookmark)
def bookmark_save(sender, **kwargs):
    if created:
        print "Received a hook for a new Bookmark!"
        print instance.url
    else:
        print "Received a hook for an old Bookmark."
