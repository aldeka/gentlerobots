from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_function
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from bmarks.models import Bookmark, Tag, Human, Address, Subscriber, Subscription
from bmarks.forms import BookmarkForm
    
def bmark_list(request, username=None, tag=None):
    # default behavior: show all bookmarks
    bookmarks = Bookmark.objects.all()
    form = BookmarkForm()
    human = None
    mine = False
    if request.user.is_authenticated():
        human = Human.objects.get(username=request.user.username)
    
    # get all for a given username
    if username:
        user = get_object_or_404(Human, username=username)
        bookmarks = bookmarks.filter(owner=user.address)
        if username == request.user.username:
            mine = True
    
    # get all with a certain tag
    elif tag:
        bookmarks = bookmarks.filter(tags=tag)
    
    # show my bookmarks plus those of my subscriptions
    elif request.user.is_authenticated():
        subscriptions = Subscription.objects.filter(the_person_listening=human)
        bookmarks = bookmarks.filter(owner=human.address)
        for subscription in subscriptions:
            bookmarks = bookmarks.filter(owner=subscription) | bookmarks
        
        
    context = {
        'bookmarks': bookmarks.order_by('-time'),
        'tags': Tag.objects.all(),
        'human': human,
        'form': form,
        'mine': mine,
    }
    return render(request, 'listing.html', context)
    
def bmark_list_mine(request):
    if user:
        return bmark_list(request, user.username)
    else:
        return bmark_list(request)
        
def login(request):
    if request.POST:
        print request.POST
        username = request.POST['username']
        password = request.POST['password']
        if request.POST['form-type'] == 'signup':
            if not Human.objects.get(username=username):
                a = Address(username=username, domain='localhost')
                a.save()
                h = Human(username=username, password=password, address=a)
                h.save()
                login_function(request, h)
                return redirect('home')
            else:
                return redirect('login')
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                login_function(request, user)
                return redirect('home')
            else:
                return redirect('login')
    else:
        new_user_form = UserCreationForm()
        login_form = AuthenticationForm()
        context = {
            'new_user_form': new_user_form,
            'login_form': login_form,
        }
        return render(request, 'registration/login.html', context)

@login_required 
def add_subscription(request):
    pass

@login_required
def new_bookmark(request):
    pass

@login_required
def delete_bookmark(request):
    if request.POST:
        pass
    pass
