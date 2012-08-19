from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from bmarks.models import Bookmark, Tag, Human, Address, Subscriber, Subscription
    
def bmark_list(request, username=None, tag=None):
    # default behavior: show all bookmarks
    bookmarks = Bookmark.objects.all()
    human = None
    if request.user.is_authenticated():
        human = Human.objects.get(username=request.user.username)
    
    # get all for a given username
    if username:
        owner = get_object_or_404(Human, username=username)
        bookmarks = bookmarks.filter(owner=owner.address)
    
    # get all with a certain tag
    elif tag:
        bookmarks = bookmarks.filter(tags=tag)
    
    # show my bookmarks plus those of my subscriptions
    elif request.user.is_authenticated():
        subscriptions = Subscription.objects.get(the_person_listening=human)
        subscribed_bookmarks = []
        for subscription in subscriptions:
            subscribed_bookmarks = bookmarks.filter(owner=subscription) + subscribed_bookmarks
        own_bookmarks = bookmarks.filter(owner=human.address)
        bookmarks = subscribed_bookmarks + own_bookmarks
        
    context = {
        'bookmarks': bookmarks,
        'tags': Tag.objects.all(),
        'human': human,
    }
    return render(request, 'listing.html', context)
    
def bmark_list_mine(request):
    if user:
        return bmark_list(request, user.username)
    else:
        return bmark_list(request)
    
def add_subscription(request):
    pass
    
def new_bookmark(request):
    pass
    
def delete_bookmark(request, bmark_id):
    pass
