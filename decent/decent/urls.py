from django.conf.urls import patterns, include, url
# import bmarks

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'decent.views.home', name='home'),
    # url(r'^decent/', include('decent.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    '''
    ### User-facing (mostly) URLs: ###
    
    url(r'^$', 'decent.views.bmark_list', name='home'),  # shows my + subscriptions if logged in, all on this install if logged out
    url(r'^me/$', 'bmarks.views.bmark_list_mine', name='bmark_list_mine'),
    url(r'^human/<username>/$', 'bmarks.views.bmark_list', name='bmark_list_by_user'),
    url(r'^tag/<tag>/$', 'bmarks.views.bmark_list', name='bmark_list_by_tag'),
    url(r'^subscribe/$', 'bmarks.views.add_subscription', name='subscribe_page'),
    url(r'^subscribe/<domain>/<username>/$', 'bmarks.views.add_subscription', name='add_subscription'),
    url(r'^new/$', 'bmarks.views.new_bookmark', name='new_bookmark'),  # typically not called via own template
    # url(r'^edit/<bmark_id>/$', 'bmarks.views.edit_bookmark', name='edit_bookmark'), ** hold off until other things work
    url(r'^delete/<bmark_id>/$', 'bmarks.views.delete_bookmark', name='delete_bookmark'),  # not a separate template
    
    Login/sign up

    **Copy someone else's bookmark to mine, with my own tags etc.
    
    ### Federation API URLs: ###
    
    
    '''
    
)
