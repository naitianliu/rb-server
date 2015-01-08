from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from mainapp.views import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rb_server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', test),
    url(r'^user/login/$', login),
    url(r'^user/logout/$', logout),
    url(r'^user/profile/$', show_profile),
    url(r'^user/records/$', rating_records),
    url(r'^display/nearby/beauties/$', display_nearby_beauties),
    url(r'^display/all/beauties/$', display_all_beauties),
    url(r'^display/nearby/rank/$', nearby_rank_list),
    url(r'^display/all/rank/$', all_rank_list),
    url(r'^user/flower/limit/update/$', flower_limit_update),
    url(r'^user/score/calculate/$', cal_user_score),
    url(r'^global/update/$', update_global),
    url(r'^user/buy/flowers$', buy_flowers),
)

urlpatterns += staticfiles_urlpatterns()