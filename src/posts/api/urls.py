# from .views import PostListAPIView, PostDetailAPIView, PostDeleteAPIView, PostUpdateAPIView
from django.urls import path, include
from .views import PostViewSet, CommentListAPIView, CommentCreateAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')


app_name = "posts-api"

urlpatterns = [
    path("", include(router.urls)),
    path("comments/<slug>/comments/",
         CommentListAPIView.as_view(), name="comment-list"),
    path("comments/<slug>/create/",
         CommentCreateAPIView.as_view(), name="comment-create"),
]
