from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf.urls.i18n import i18n_patterns
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    ############## Italian ##################
    url(r'^it/trova/(?P<company>[a-z0-9\+\.\'\(\)]*)/(?P<id>\d+)/(?P<product>[a-z\+]*)/', 'it.views.bioshow', name='vetrina'),
    url(r'^it/cercabiomassa/(?P<product>[a-z\+\-]*)/(?P<region>[a-z\+\-]*)/(?P<province>[a-z\+\-]*)/', 'it.views.find'),
    url(r'^it/cercabiomassa/(?P<product>[a-z\+\-]*)/(?P<region>[a-z\+\-]*)/', 'it.views.find'),
    url(r'^it/cercabiomassa/(?P<product>[a-z\+\-]*)/', 'it.views.find'),
    url(r'^it/cercabiomassa/', 'it.views.find', name='cerca'),
    url(r'^it/trovabiomassa/(?P<product>[a-z\+\-]*)/(?P<region>[a-z\+\-]*)/(?P<province>[a-z\+\-]*)/', 'it.views.results'),
    url(r'^it/trovabiomassa/(?P<product>[a-z\+\-]*)/(?P<region>[a-z\+\-]*)/', 'it.views.results'),
    url(r'^it/trovabiomassa/(?P<product>[a-z\+\-]*)/', 'it.views.results'),
    url(r'^it/trovabiomassa/', 'it.views.JsonProvider', name='risultati'),
    url(r'^it/coordinate/', 'it.views.coordinates', name='coordinate'),

    #static content
    url(r'^it/credits/', 'it.pages.about'),
    url(r'^it/privacy/', 'it.pages.privacy'),
    url(r'^it/energia/', 'it.pages.energia'),
    url(r'^it/contacts/', 'it.pages.contacts'),
    url(r'^static/(?P<path>.*)$','django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

    # users
    url(r'^it/register', 'it.users.auth.subscription'),
    url(r'^it/subscribe', 'it.users.auth.newsletter'),
    url(r'^it/accounts/login', 'it.users.auth.login_user'),
    url(r'^it/accounts/logout/$', 'it.users.auth.logout_user'),
    url(r'^it/accounts/database/product/remove/(?P<product_id>\d+)', 'it.users.auth.remove_product'),
    url(r'^it/accounts/database/product/modify/(?P<product_id>\d+)/(?P<reseller_id>\d+)', 'it.users.auth.modify_product'),
    url(r'^it/accounts/database/product/add/(?P<reseller_id>\d+)', 'it.users.auth.add_product'),
    url(r'^it/accounts/database/transport/add/(?P<reseller_id>\d+)', 'it.users.auth.add_transport'),
    #tmap
    url(r'^it/profile/tmap', 'it.tmap.views.page', name='tmap'),
    #profile
    url(r'^it/profile', 'it.users.auth.main_profile'),

    # pwd recover
    url(r'^it/user/password/reset/$', 
       'django.contrib.auth.views.password_reset', 
      {'post_reset_redirect' : '/user/password/reset/done/', 'template_name': 'users/registration/password_reset_form.html'},
      name='password_reset'),
    url(r'^it/user/password/reset/done/$',
       'django.contrib.auth.views.password_reset_done', {'template_name': 'users/registration/password_reset_done.html'}, 
      name='password_reset_done'),
    url(r'^it/user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
       'django.contrib.auth.views.password_reset_confirm', 
      {'post_reset_redirect' : '/user/password/done/', 'template_name': 'users/registration/password_reset_confirm.html'}, 
        name='password_reset_confirm'),
    url(r'^it/user/password/done/$', 
        'django.contrib.auth.views.password_reset_complete', {'template_name': 'users/registration/password_reset_complete.html'}, 
        name='password_reset_complete'),

    url(r'^it/sitemap\.xml$', 'it.sitemap.Sitemap'),
    url(r'^it/robots.txt$', 'it.sitemap.Robots'),

    ############## Spanish ##################
    url(r'^es/encontra/(?P<company>[a-z0-9\+\.\'\(\)]*)/(?P<id>\d+)/(?P<product>[a-z\+]*)/', 'es.views.bioshow', name='vetrina'),
    url(r'^es/busquabiomasa/(?P<product>[a-z\+\-]*)/(?P<region>[a-z\+\-]*)/(?P<province>[a-z\+\-]*)/', 'es.views.find'),
    url(r'^es/busquabiomasa/(?P<product>[a-z\+\-]*)/(?P<region>[a-z\+\-]*)/', 'es.views.find'),
    url(r'^es/busquabiomasa/(?P<product>[a-z\+\-]*)/', 'es.views.find'),
    url(r'^es/busquabiomasa/', 'es.views.find', name='cerca'),
    url(r'^es/encontrabiomasa/(?P<product>[a-z\+\-]*)/(?P<region>[a-z\+\-]*)/(?P<province>[a-z\+\-]*)/', 'es.views.results'),
    url(r'^es/encontrabiomasa/(?P<product>[a-z\+\-]*)/(?P<region>[a-z\+\-]*)/', 'es.views.results'),
    url(r'^es/encontrabiomasa/(?P<product>[a-z\+\-]*)/', 'es.views.results'),
    url(r'^es/encontrabiomasa/', 'es.views.JsonProvider', name='risultati'),
    url(r'^es/coordinadas/', 'es.views.coordinates', name='coordinate'),

    #static content
    url(r'^es/credits/', 'es.pages.about'),
    url(r'^es/privacy/', 'es.pages.privacy'),
    url(r'^es/energia/', 'es.pages.energia'),
    url(r'^es/contacts/', 'es.pages.contacts'),
    url(r'^static/(?P<path>.*)$','django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

    # users
    url(r'^es/register', 'es.users.auth.subscription'),
    url(r'^es/subscribe', 'es.users.auth.newsletter'),
    url(r'^es/accounts/login', 'es.users.auth.login_user'),
    url(r'^es/accounts/logout/$', 'es.users.auth.logout_user'),
    url(r'^es/accounts/database/product/remove/(?P<product_id>\d+)', 'es.users.auth.remove_product'),
    url(r'^es/accounts/database/product/modify/(?P<product_id>\d+)/(?P<reseller_id>\d+)', 'es.users.auth.modify_product'),
    url(r'^es/accounts/database/product/add/(?P<reseller_id>\d+)', 'es.users.auth.add_product'),
    url(r'^es/accounts/database/transport/add/(?P<reseller_id>\d+)', 'es.users.auth.add_transport'),
    #tmap
    url(r'^es/profile/tmap', 'es.tmap.views.page', name='tmap'),
    #profile
    url(r'^es/profile', 'es.users.auth.main_profile'),

    # pwd recover
    url(r'^es/user/password/reset/$', 
       'django.contrib.auth.views.password_reset', 
      {'post_reset_redirect' : '/user/password/reset/done/', 'template_name': 'users/registration/password_reset_form.html'},
      name='password_reset'),
    url(r'^es/user/password/reset/done/$',
       'django.contrib.auth.views.password_reset_done', {'template_name': 'users/registration/password_reset_done.html'}, 
      name='password_reset_done'),
    url(r'^es/user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
       'django.contrib.auth.views.password_reset_confirm', 
      {'post_reset_redirect' : '/user/password/done/', 'template_name': 'users/registration/password_reset_confirm.html'}, 
        name='password_reset_confirm'),
    url(r'^es/user/password/done/$', 
        'django.contrib.auth.views.password_reset_complete', {'template_name': 'users/registration/password_reset_complete.html'}, 
        name='password_reset_complete'),

    url(r'^es/sitemap\.xml$', 'es.sitemap.Sitemap'),
    url(r'^es/robots.txt$', 'es.sitemap.Robots'),

    # internazionalization
    #url(r'^/es/', include(es.urls)),
    url(r'^it/$', 'it.views.home', name='home_it'),
    url(r'^es/$', 'es.views.home', name='home_es'),

    # administration urls
    url(r'^admin/', include(admin.site.urls)),

    #url(r'^sitemap\.xml$', 'sitemap.Sitemap'),
    #url(r'^robots.txt$', 'sitemap.Robots'),
    url(r'^$', 'it.views.home', name='home_it'),
    url(r'^', include('cms.urls')),
    #url(r'.*', 'service.views.home', name='home'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
)
