from django.contrib import admin
from django.conf.urls import url, include
from .views import *
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='blog/index.html'), name='index'),
    url(r'^blogs/$', BlogListView.as_view(), name="blog-list"),
    url(r'^blogs/(?P<pk>[0-9]+)/$', BlogDetailView.as_view(), name='blog-details'),
    url(r'^posts/$', PostListView.as_view(), name='post-list'),
    url(r'^posts/(?P<pk>[0-9]+)/$', PostDetailView.as_view(), name='post-details'),
    url(r'^post/new/$', PostCreateView.as_view(), name='post-create'),
    # url(r'^posts/(?P<post_id>[0-9]+)/comments/$', CommentListView.as_view(), name='comment-list')
]
