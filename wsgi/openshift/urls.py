from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf.urls.i18n import i18n_patterns
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^trova/(?P<company>[a-z0-9\+\.\'\(\)]*)/(?P<id>\d+)/(?P<product>[a-z\+]*)/', 'service.views.bioshow', name='vetrina'),
    #url(r'^cercabiomassa/(?P<product>[a-z\+\-]*)/(?P<region>[a-z\+\-]*)/(?P<province>[a-z\+\-]*)/', 'service.views.find'),
    #url(r'^cercabiomassa/(?P<product>[a-z\+\-]*)/(?P<region>[a-z\+\-]*)/', 'service.views.find'),
    #url(r'^cercabiomassa/(?P<product>[a-z\+\-]*)/', 'service.views.find'),
    #url(r'^cercabiomassa/', 'service.views.find', name='cerca'),
    #url(r'^trovabiomassa/(?P<product>[a-z\+\-]*)/(?P<region>[a-z\+\-]*)/(?P<province>[a-z\+\-]*)/', 'service.views.results'),
    #url(r'^trovabiomassa/(?P<product>[a-z\+\-]*)/(?P<region>[a-z\+\-]*)/', 'service.views.results'),
    #url(r'^trovabiomassa/(?P<product>[a-z\+\-]*)/', 'service.views.results'),
    #url(r'^trovabiomassa/', 'service.views.JsonProvider', name='risultati'),
    #url(r'^coordinate/', 'service.views.coordinates', name='coordinate'),

    #static content
    #url(r'^credits/', 'service.pages.about'),
    #url(r'^privacy/', 'service.pages.privacy'),
    #url(r'^energia/', 'service.pages.energia'),
    #url(r'^contacts/', 'service.pages.contacts'),
    #url(r'^static/(?P<path>.*)$','django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

    # users
    #url(r'^register', 'service.users.auth.subscription'),
    #url(r'^subscribe', 'service.users.auth.newsletter'),
    #url(r'^accounts/login', 'service.users.auth.login_user'),
    #url(r'^accounts/logout/$', 'service.users.auth.logout_user'),
    #url(r'^accounts/database/product/remove/(?P<product_id>\d+)', 'service.users.auth.remove_product'),
    #url(r'^accounts/database/product/modify/(?P<product_id>\d+)/(?P<reseller_id>\d+)', 'service.users.auth.modify_product'),
    #url(r'^accounts/database/product/add/(?P<reseller_id>\d+)', 'service.users.auth.add_product'),
    #url(r'^accounts/database/transport/add/(?P<reseller_id>\d+)', 'service.users.auth.add_transport'),
    #tmap
    #url(r'^profile/tmap', 'tmap.views.page', name='tmap'),
    #profile
    #url(r'^profile', 'service.users.auth.main_profile'),

    # pwd recover
    #url(r'^user/password/reset/$', 
    #   'django.contrib.auth.views.password_reset', 
    #  {'post_reset_redirect' : '/user/password/reset/done/', 'template_name': 'users/registration/password_reset_form.html'},
    #  name='password_reset'),
    #url(r'^user/password/reset/done/$',
    #   'django.contrib.auth.views.password_reset_done', {'template_name': 'users/registration/password_reset_done.html'}, 
    #  name='password_reset_done'),
    #url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
    #   'django.contrib.auth.views.password_reset_confirm', 
    #  {'post_reset_redirect' : '/user/password/done/', 'template_name': 'users/registration/password_reset_confirm.html'}, 
    #    name='password_reset_confirm'),
    #url(r'^user/password/done/$', 
    #    'django.contrib.auth.views.password_reset_complete', {'template_name': 'users/registration/password_reset_complete.html'}, 
    #    name='password_reset_complete'),


    # internazionalization
    #url(r'^/es/', include(es.urls)),
    url(r'^/it/', include('it.urls')),

    # administration urls
    url(r'^admin/', include(admin.site.urls)),

    #url(r'^sitemap\.xml$', 'sitemap.Sitemap'),
    #url(r'^robots.txt$', 'sitemap.Robots'),
    #url(r'^$', 'service.views.home', name='home'),
    url(r'^', include('cms.urls')),
    #url(r'.*', 'service.views.home', name='home'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
)
