from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_function
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from bmarks.models import Bookmark, Tag, Human, Address, Subscriber, Subscription
from bmarks.forms import BookmarkForm, SubscriptionForm
import datetime
from itertools import chain
from operator import attrgetter
    
def bmark_list(request, username=None, tag=None, mode=None):
    if request.method == 'POST':
        form = BookmarkForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            tags = form.cleaned_data['tags']
            description = form.cleaned_data['description']
            human = request.user.human
            b = Bookmark(url=url, owner=human.address)
            if description:
                b.description = description
            if tags:
                b.save()
                tag_list = tags.split(',')
                print tags
                for tag in tag_list:
                    tag = tag.strip()
                    if Tag.objects.filter(name=tag):
                        t = Tag.objects.get(name=tag)
                    else:
                        t = Tag(name=tag)
                        t.save()
                    b.tags.add(t)
            b.save()
        else:
            print form
        return redirect('home')
    elif request.method == 'GET':
        # default behavior: show all bookmarks
        bookmarks = Bookmark.objects.all()
        form = BookmarkForm()
        human = None
        subscriptions = None
        
        if request.user.is_authenticated():
            human = Human.objects.get(username=request.user.username)
            if not mode:
                mode = "subs"
        else:
            if mode=="mine" or mode=="subs":
                redirect('home')
            else:
                mode="all"
        
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
        elif mode == 'subs':
            subscriptions = Subscription.objects.filter(the_person_listening=human)
            print subscriptions
            my_bookmarks = bookmarks.filter(owner=human.address)
            c = chain(my_bookmarks, [])
            for subscription in subscriptions:
                if subscription.domain == 'localhost':
                    h = Human.objects.get(username=subscription.username)
                    c = chain(c, bookmarks.filter(owner=h.address))
                else:
                    c = chain(c, bookmarks.filter(remote_owner=subscription))
            
            bookmarks = sorted(c, key=attrgetter('time'))
                    
        # show just my bookmarks
        elif mode == 'mine':
            bookmarks = bookmarks.filter(owner=human.address)
        
        context = {
            'bookmarks': bookmarks,
            'tags': Tag.objects.all(),
            'subscriptions': subscriptions,
            'human': human,
            'form': form,
            'mode': mode,
        }
        return render(request, 'listing.html', context)
        
def login(request):
    if request.method == 'POST':
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
    if request.method == "POST":
        human = request.user.human
        if request.POST['form-type']:
            form = SubscriptionForm(request.POST)
            if form.is_valid():
                address = form.cleaned_data['full_address'].split('@')
                if len(address) <= 2:
                    username = address[0]
                    domain = address[1]
        elif request.is_ajax():
            username = request.POST['username']
            domain = request.POST['domain']
            
        if domain == "localhost":
            h = get_object_or_404(Human, username=username)
            subscriber = Subscriber(username=human.username, domain="localhost", the_person_sending=h, last_updated=datetime.datetime.now())
            subscriber.save()
        else:
            # ping them to make a subscriber
            pass
        subscription = Subscription(username=username, domain=domain, the_person_listening=human, last_received_update=datetime.datetime.now())
        subscription.save()
        return redirect('subscription_page')

    else:
        if request.user.is_authenticated():
            human = request.user.human
            subscriptions = Subscription.objects.filter(the_person_listening=human)
            form = SubscriptionForm()
            context = {
                'subscriptions': subscriptions,
                'human': human,
                'form': form,
            }
            return render(request, 'subscriptions.html', context)
        else:
            redirect('login')
        

@login_required
def new_bookmark(request):
    pass

def delete_bookmark(request):
    message = ''
    mime='text'
    if request.is_ajax() and request.method == 'POST':
        if request.POST['bookmark_id']:
            bookmark_id = request.POST['bookmark_id'][9:]
            b = Bookmark.objects.get(pk=int(bookmark_id))
            b.delete()
            message = "Successfully deleted bookmark #" + bookmark_id
    return HttpResponse(message,mime)
    
def delete_subscription(request):
    message = ''
    mime='text'
    human = request.user.human
    if request.is_ajax() and request.method == 'POST':
        if request.POST['subscription_id']:
            subscription_id = request.POST['subscription_id'][13:]
            subscription = Subscription.objects.get(pk=int(subscription_id))
            if subscription.domain == "localhost":
                h = Human.objects.get(username=subscription.username)
                subscriber = Subscriber.objects.filter(username=human.username).filter(the_person_sending=h)[0]
                subscriber.delete()
            else:
                #ping other service
                pass
            subscription.delete()
            message = "Successfully deleted subscription #" + subscription_id
    return HttpResponse(message,mime)
