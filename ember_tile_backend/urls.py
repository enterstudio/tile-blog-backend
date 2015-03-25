from django.conf.urls import patterns, include, url
from django.contrib import admin
from app.views import UserAuthenticationView
from app.serializers import PostList, PostDetail, ImageList, ImageDetail, BloggerDetail

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ember_tile_backend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/auth/$', UserAuthenticationView.as_view()),
    url(r'^api/posts/$', PostList.as_view(), name="posts-list"),
    url(r'^api/posts/(?P<pk>[0-9]+)/$', PostDetail.as_view(), name="posts-detail"),
    url(r'^api/images/$', ImageList.as_view(), name="images-list"),
    url(r'^api/images/(?P<pk>[0-9]+)/$', ImageDetail.as_view(), name="images-detail"),
    url(r'^api/bloggers/(?P<pk>[0-9]+)/$', BloggerDetail.as_view(), name="blogger-detail")
)
