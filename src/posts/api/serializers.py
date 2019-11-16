from rest_framework import serializers
from ..models import Post, Comment
from django.utils.timezone import now
from profiles.api.serializers import ProfileSerializer




class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        many=False, read_only=True)
    created = serializers.SerializerMethodField()
    post = serializers.StringRelatedField(
        many=False, read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def get_created(self, obj):
        return obj.created.strftime("%m/%d/%Y, %H:%M:%S")

class PostListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        many=False, read_only=True)
    profile = ProfileSerializer(read_only=True, many=False)
    days_since_created = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    comments = CommentSerializer(read_only=True, many=True)
    user_has_liked = serializers.SerializerMethodField()
    user_is_post_author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'body', 'author', 'profile', 'image', 
                  'no_of_likes', 'user_has_liked', 'no_of_comments',
                  'days_since_created', 'comments', 'created', 'user_is_post_author')

    def get_days_since_created(self, obj):
        return "{} days".format((now() - obj.created).days)

    def get_created(self, obj):
        return obj.created.strftime("%m/%d/%Y, %H:%M:%S")

    def get_liked(self, obj):
        names = []
        for name in obj.liked.all():
            names.append(name.username)
        return names

    def get_user_has_liked(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            return obj.liked.filter(pk=request.user.pk).exists()
        return None

    def get_user_is_post_author(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            return obj.author == user


class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        many=False, read_only=True)
    profile = ProfileSerializer(read_only=True, many=False)
    liked = serializers.SerializerMethodField()
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'author', 'profile', 'image',
                  'liked', 'no_of_likes', 'no_of_comments', 'comments']

    def get_liked(self, obj):
        names = []
        for name in obj.liked.all():
            names.append(name.username)
        return names
