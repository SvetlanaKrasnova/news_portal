from django.urls import path
from .views import PostList, PostDetail, CreatePost, PostEdit, PostDelete

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('news/create/', CreatePost.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

    path('articles/create/', CreatePost.as_view(), name='post_create'),
    path('articles/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('search/', PostList.as_view(), name='post_list'),
]
