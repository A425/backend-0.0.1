from django.conf.urls import patterns, include, url
from backend.views import *
from users.views import *
from articles.views import *
import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'backend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login),
    url(r'^checkCode/$', getCheckCode),

    url(r'^newuser$', createUser),
    url(r'^signin$', signIn),
    url(r'^validate$', userValidate),
    url(r'^testToken/$', testToken),

    url(r'^postArticle$', postArticle),
    url(r'^getArticles$', getArticles),
    url(r'^testArticle/$', testArticle),

    url(r'^downloadapk$', downloadapk),
    url(r'^getMatrixCode$', getMatrixCode),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT })
)
