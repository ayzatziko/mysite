from django.urls import path, re_path
from blog import views

app_name = 'blog'

urlpatterns = [
  path('', views.PostsListView.as_view(), name='posts_list'),
  re_path(r'^post/(?P<pk>\d+)$', views.PostDetail.as_view(), name='post_detail'),
  path('post/new', views.CreatePostView.as_view(), name='create_post'),
  re_path(r'^post/(?P<pk>\d+)/edit$', views.UpdatePostView.as_view(), name='update_post'),
  re_path(r'^post/(?P<pk>\d+)/remove$', views.DeletePostView.as_view(), name='remove_post'),
  path('drafts', views.DraftsListView.as_view(), name='drafts'),
  re_path(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
  re_path(r'^comments/(?P<pk>\d+)/approve$', views.approve_comment, name='approve_comment'),
  re_path(r'^comments/(?P<pk>\d+)/remove$', views.remove_comment, name='remove_comment'),
  re_path(r'^post/(?P<pk>\d+)/publish$', views.publish_post, name='publish_post'),
  path('about', views.AboutView.as_view(), name='about'),
]