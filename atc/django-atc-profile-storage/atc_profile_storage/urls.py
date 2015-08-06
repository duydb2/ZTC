from django.conf.urls import url
from atc_profile_storage.views import ProfilesApi, ProfileApi

urlpatterns = [
    url(r'^$', ProfilesApi.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', ProfileApi.as_view()),
]
