from django.conf.urls import patterns, include, url
from backend.views import *
from users.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'backend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login),
    url(r'^checkCode/$', getCheckCode),
    url(r'^register/$', register),

    url(r'^newuser$', createUser),
    url(r'^signin$', signIn),
    # url(r'^validate$', userValidate),
    url(r'^test/$', testData),
)
