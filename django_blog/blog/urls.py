from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import PostsByTagView, PostCreateView, PostDeleteView, PostDetailView, PostListView, PostUpdateView, CommentCreateView, CommentDeleteView, CommentUpdateView

# urlpatterns = [
#     path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
#     path('register/', views.register, name='register'),
#     path('profile/', views.profile, name='profile'),
#     path('posts/', PostListView.as_view(), name='post_list'),
#     path('posts/new/', PostCreateView.as_view(), name='post_new'),
#     path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
#     path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
#     path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
#     path('posts/<int:post_pk>/comments/new/', CommentCreateView.as_view(), name='comment_new'),
#     path('comments/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_edit'),
#     path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
#     path('tags/', views.PostsByTagView.as_view(), name='tag_list'),               
#     path('tags/<slug:tag_slug>/', views.PostsByTagView.as_view(), name='posts_by_tag'),
#     path('search/', views.search_view, name='search'),
#     path('posts/', views.PostListView.as_view(), name='post_list'),
#     path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
# ]

 urlpatterns = [  
    path('register/', register_view, name='register'),
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='blog/logged_out.html'), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comments/new/',CommentCreateView.as_view(), name='add-comment'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/',CommentDeleteView.as_view(), name='comment-delete'),
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='posts-by-tag'),
     path('search/', PostSearchView.as_view(), name='post-search'),
 ]
