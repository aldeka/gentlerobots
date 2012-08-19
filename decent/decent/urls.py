from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

alphanum_plus = "[a-zA-Z0-9-_]+"

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'decent.views.home', name='home'),
    # url(r'^decent/', include('decent.foo.urls')),
    
    ### User-facing (mostly) URLs: ###
    
    url(r'^$', 'bmarks.views.crud.bmark_list', name='home'),  # shows my + subscriptions if logged in, all on this install if logged out
    url(r'^about/$', 'django.views.generic.simple.direct_to_template', {'template': 'about.html',}, name='about'),
    url(r'^me/$', 'bmarks.views.crud.bmark_list_mine', name='bmark_list_mine'),
    url(r'^all/$', 'bmarks.views.crud.bmark_list', name='bmark_list_all'),
    url(r'^human/(?P<username>'+alphanum_plus+')/$', 'bmarks.views.crud.bmark_list', name='bmark_list_by_user'),
    url(r'^tag/(?P<tag>'+alphanum_plus+')/$', 'bmarks.views.crud.bmark_list', name='bmark_list_by_tag'),
    url(r'^subscriptions/$', 'bmarks.views.crud.add_subscription', name='subscribe_page'),
    url(r'^subscribe/(?P<domain>\S+)/(?P<username>'+alphanum_plus+')/$', 'bmarks.views.crud.add_subscription', name='add_subscription'),
    url(r'^new/$', 'bmarks.views.crud.new_bookmark', name='new_bookmark'),  # typically not called via own template
    # url(r'^edit/(?P<bmark_id>\d+)/$', 'bmarks.views.crud.edit_bookmark', name='edit_bookmark'), ** hold off until other things work
    url(r'^delete/$', 'bmarks.views.crud.delete_bookmark', name='delete_bookmark'),  # not a separate template
    
    # Login/sign up
    
    url(r'^login/$', 'bmarks.views.crud.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),

    # **Copy someone else's bookmark to mine, with my own tags etc.
    
    ### Federation API URLs: ###
    
    url(r'^human/(?P<username>'+alphanum_plus+')/update/$', 'bmarks.views.federators.receive_updates', name='receive_updates'),  # pings from subscribed-to users go here
    url(r'^human/(?P<username>'+alphanum_plus+')/subscribe/$', 'bmarks.views.federators.update_subscriber_info', name='update_subscriber_info'),  # pings when someone new subscribes or unsubscribes go here
    url(r'^human/(?P<username>'+alphanum_plus+')/get/last/(?P<num_updates>\d+)$', 'bmarks.views.federators.fetch_last_n_bmarks', name='fetch_last_n_bmarks'),  # request arbitrary number of bookmarks, reverse-chron order, get some json
    #url(r'^human/(?P<username>'+alpha-num_plus+')/get/since/<datetime>$', 'bmarks.views.fetch_bmarks_by_date', name='fetch_bmarks_by_date'),  # request all bookmarks after a certain datetime, get some json

)
