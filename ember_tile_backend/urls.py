from django.conf.urls import patterns, include, url
from django.contrib import admin
from app.views import UserAuthenticationView
from app.serializers import PostList, ImageList

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ember_tile_backend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/auth/', UserAuthenticationView.as_view()),
    url(r'^api/posts/', PostList.as_view(), name="posts-list"),
    url(r'^api/images/', ImageList.as_view(), name="images-list")
)
