from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView)
from ..models import Post, Comment
from .serializers import PostListSerializer, PostDetailSerializer, CommentSerializer
from .perimissions import IsOwnerOrReadOnly
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly)
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import status, viewsets
from django.contrib.auth.models import User
import json
from .pagination import CustomPagination
from profiles.models import Profile
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostDetailSerializer

    def perform_create(self, serializer):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        serializer.save(author=user, profile=profile)

    def get_queryset(self):
        query = self.request.GET.get('search', None)
        if query is not None:
            queryset = Post.objects.filter(
                Q(title__icontains=query) | Q(body__icontains=query)).distinct()
        else:
            queryset = Post.objects.all()
        return queryset

    @action(detail=True, methods=['post'])
    def like_create(self, request, slug=None, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        user = self.request.user
        post = get_object_or_404(Post, slug=slug)
        if user in post.liked.all():
            post.liked.remove(request.user)
            value = "Unlike"
        else:
            post.liked.add(request.user)
            value = "Like"
        serializer = PostListSerializer(post)
        valSerializer = json.dumps(value)
        response = {
            'value': valSerializer,
            'result': serializer.data
        }
        return Response(response, status=status.HTTP_201_CREATED)


class CommentListAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    # pagination_class = CustomPagination

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug", None)
        return Comment.objects.filter(post__slug=kwarg_slug).order_by("-created")


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    # pagination_class = CustomPagination

    def perform_create(self, serializer):
        request_user = self.request.user
        kwarg_slug = self.kwargs.get('slug', None)
        post = get_object_or_404(Post, slug=kwarg_slug)
        serializer.save(author=request_user, post=post)
