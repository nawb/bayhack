from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from browse import views as browse_views
from login import views as login_views
from addurl import views as addurl_views


#from browse import views
#from login import views


urlpatterns = patterns('',

	url(r'^diary/$','diary.views.diary_home_page'),
	url(r'^diary/reflect/(?P<surah>[0-9]+)/(?P<ayah>[0-9]+)$','diary.views.diary_reflect_page'),
	url(r'^diary/read/(?P<surah>[0-9]+)/(?P<ayah>[0-9]+)$','diary.views.diary_read_page'),
	url(r'^diary/find/$','diary.views.diary_find_page'),
	url(r'^diary/search$','diary.views.search'),

    url(r'^mobile/$', login_views.mobile_home),
    url(r'^home-submit/$', login_views.submission),
    url(r'^feedback/browse/$', login_views.feedback_from_browse),
    url(r'^feedback/broken/$', login_views.feedback_broken_link),
    url(r'^approve/$', browse_views.approve),
    url(r'^approve-form/$', browse_views.approve_form),
    url(r'^approve-form-delete/$', browse_views.approve_form_delete),
    url(r'^thanks/$', login_views.thanks),
	url(r'^logout/$', login_views.logout, name='logout'),

    url('^', include('django.contrib.auth.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),		#this is the one that handles all social logins

    url(r'^update-score/$', browse_views.update_score),
    
    url(r'^$', 'login.views.home', name='home'),
    url(r'^browse/$', browse_views.browse),
    url(r'^browse/(?P<id>[0-9]+)/$', browse_views.browse),
    url(r'^generate-title/$', addurl_views.generate_titles),
    url(r'^generate-tags/$', addurl_views.generate_tags),
    url(r'^revise/$', browse_views.revise_page),
    url(r'^revise-next/$', browse_views.revise_next),
    #url(r'^complete/facebook/$', browse_views.browse),
    #url(r'^blog/', include('blog.urls')),
    url(r'^all_login/$', auth_views.login, {'extra_context': {'next':'/browse'}}),
#    url(r'^mylogin/$', login_views.login),
    url(r'^stumble/$', browse_views.stumble),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^addurl/(?P<submit>.*)', addurl_views.add),
    url(r'^next/$', browse_views.stumble),
    url(r'^add/$', browse_views.add),
    url(r'^add-arabic/$', browse_views.add_arabic),
    url(r'^add-form/$', browse_views.add_form),
    url(r'^add-form-arabic/$', browse_views.add_form_arabic),
    url(r'^next/$', 'browse.views.stumble'),
    url(r'^addurl/(?P<submit>.*)', addurl_views.add),
    url(r'^next/(?P<id>[0-9]+)/$', browse_views.stumble),
    url(r'^analytics/$', browse_views.analytics),
    url(r'^leader/$', browse_views.leader),
    url(r'^profile/$', browse_views.profile),
#    url(r'^quicklogin/$', login_views.quicklogin),
#    url(r'^login_old/$', login_views.login_form),
#    url(r'^login_process/$', login_views.LoginButton),
    url(r'^fbjava/$', login_views.fbjava),
    url(r'^upvote/(?P<id>[0-9]+)/$', browse_views.upvote),
    url(r'^downvote/(?P<id>[0-9]+)/$', browse_views.downvote),                   
    url(r'^delete-vote/(?P<id>[0-9]+)/$', browse_views.delete_vote),                   
    url(r'^view/(?P<id>[0-9]+)/$', browse_views.view_page),                   
                  
)
