from django.conf.urls import include, url
from django.contrib import admin
import django.views
import asa18.views
import settings_dev

# app_name = 'asa18'
urlpatterns = [
    # Examples:
    # url(r'^$', 'asa18.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^tinymce/', include('tinymce.urls')),

    url(r'^captcha/', include('captcha.urls')),

    url(r'^register/1/$', asa18.views.register_person, name='register_person'),
    url(r'^register/2/$', asa18.views.register_meetings,
        name='register_meetings'),
    url(r'^register/3/$', asa18.views.register_presentation,
        name='register_presentation'),
    url(r'^register/4/$', asa18.views.register_events, name='register_events'),
    url(r'^register/5/$', asa18.views.register_confirm,
        name='register_confirm'),
    # url(r'^register/abort/$', asa18.views.register_abort,
    #     name='register_abort'),
    url(r'^register/$', asa18.views.register_splash, name='register_splash'),

    url(r'^(?P<meeting>[\w\-]+)/news/(?P<newsitem>[\w\-]+)$',
        asa18.views.news, name='news_meeting'),
    url(r'^(?P<meeting>[\w\-]+)/news/$', asa18.views.news_index,
        name='news_index_meeting'),

    url(r'^news/(?P<newsitem>[\w\-]+)$', asa18.views.news,
        name='news'),
    url(r'^news/$', asa18.views.news_index, name='news_index'),

    url(r'^(?P<meeting>[\w\-]+)/prizes/(?P<prize>[\w\-]+)$',
        asa18.views.prize, name='prize'),
    url(r'^(?P<meeting>[\w\-]+)/prizes/',
        asa18.views.prize_index, name='prize_index'),

    url(r'^(?P<meeting>[\w\-]+)/events/(?P<eventslug>[\w\-]+)/$',
        asa18.views.event, name='event'),
    url(r'^(?P<meeting>[\w\-]+)/events/$', asa18.views.event_index,
        name='event_index'),

    url(r'^(?P<meeting>[\w\-]+)/participants/$',
        asa18.views.meeting_participants,
        name='participants'),
    url(r'^(?P<meeting>[\w\-]+)/program/$',
        asa18.views.meeting_program,
        name='program'),
    url(r'^(?P<meeting>[\w\-]+)/posters/$',
        asa18.views.meeting_posters,
        name='posters'),

    url(r'^(?P<meeting>[\w\-]+)/policies/$', asa18.views.policy,
        name='policy'),

    url(r'^(?P<meeting>[\w\-]+)/sponsors/$', asa18.views.sponsors,
        name='sponsors'),

    url(r'^confirm_payment/$', asa18.views.confirm_payment,
        name='confirm_payment'),

    url(r'^edit_abstracts/(?P<id>[0-9]+)/$', asa18.views.edit_abstracts,
        name='edit_abstracts_alter'),
    url(r'^edit_abstracts/$', asa18.views.edit_abstracts,
        name='edit_abstracts'),

    url(r'^presentation_mgmt/(?P<pk>[0-9]*)/$',
        asa18.views.presentation_mgmt,
        name='presentation_mgmt'),

    url('^check_rego/$', asa18.views.check_rego,
        name='check_rego'),

    url('^rego_summary/$', asa18.views.rego_summary,
        name='rego_summary'),

    # Comment these out in production
    # url(r'^404/$', asa18.views.test404),
    # url(r'^500/$', asa18.views.test500),

    url(r'^(?P<meeting>[\w\-]+)/$', asa18.views.meeting_splash,
        name='meeting_splash'),

    url(r'^$', asa18.views.splash, name='splash'),
]

# Development media serving
if settings_dev.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', django.views.static.serve, {
        'document_root': settings_dev.MEDIA_ROOT})]
