from django.urls import path

from .views import (
    index, lenta_of_posts,
    post_create, DetailPostView,
    post_like, DeletePostView,
    UpdatePostView
)


app_name = 'posts'

urlpatterns = [
    path('', index, name='index'),
    path('lenta/', lenta_of_posts, name='lenta'),
    path('<int:post_pk>/', DetailPostView.as_view(), name='post-detail'),
    path('post-create/', post_create, name='post-create'),
    path('post-update/<int:post_pk>/', UpdatePostView.as_view(), name='post-update'),
    path('post-delete/<int:post_pk>/', DeletePostView.as_view(), name='post-delete'),
    path('like/<int:post_pk>/', post_like, name='like'),
]