from django.urls import path
# from django.views.decorators.cache import cache_page
from .views import PostList, PostDetail, PostCreate, PostEdit, PostDelete, CommentDelete, CommentCreate

urlpatterns = [
    # path('', cache_page(60 * 5)(PostList.as_view()), name='post_list'),
    path('', PostList.as_view(), name='post_list'),
    # path('news/<int:pk>', cache_page(60)(PostDetail.as_view()), name='post_detail'),
    path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('news/create/', PostCreate.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('news/comment_create/', CommentCreate.as_view(), name='comment_create'),
    path('news/comment_delete/<int:pk>', CommentDelete.as_view(), name='comment_delete'),

    path('articles/create/', PostCreate.as_view(), name='post_create'),
    path('articles/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('search/', PostList.as_view(), name='post_search'),
]
