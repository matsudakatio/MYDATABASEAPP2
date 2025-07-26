from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/like/', views.LikeView.as_view(), name='like'),
]