from django.urls import path
from django.views.decorators.cache import cache_page
from .views import PostList, PostDetail, CreatePost, PostEdit, PostDelete

urlpatterns = [
    path('', cache_page(60 * 5)(PostList.as_view()), name='post_list'),
    path('news/<int:pk>', cache_page(60)(PostDetail.as_view()), name='post_detail'),
    path('news/create/', CreatePost.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

    path('articles/create/', CreatePost.as_view(), name='post_create'),
    path('articles/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('search/', PostList.as_view(), name='post_search'),
]
