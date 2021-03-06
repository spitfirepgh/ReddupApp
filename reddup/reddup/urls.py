from django.conf.urls import patterns, include, url
from scru import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # ex: /
    url(r'^$', 'scru.views.index', name='index'),

    # ex: /issues/all/
    url(r'^issues/all/$', 'scru.views.all_issues', name='all_issues'),
    url(r'^issues/all/ajax/$', 'scru.views.all_issues_ajax', name='all_issues_ajax'),

    # ex: /issues/user/{user_id}
    url(r'^issues/user/(?P<user_id>\d+)/$', 'scru.views.user_issues', name='user_issues'),

    # ajax views
    url(r'^issue/open/$', 'scru.views.open_issue', name='open_issue'),
    url(r'^issue/close/$', 'scru.views.close_issue', name='close_issue'),
    url(r'^issue/(?P<issue_id>\d+)/reup/$', 'scru.views.reup_issue', name='reup_issue'),
    url(r'^issue/(?P<issue_id>\d+)/claim/$', 'scru.views.claim_issue', name='claim_issue'),
    url(r'^pledge/new/$', 'scru.views.create_pledge', name='create_pledge'),

)
