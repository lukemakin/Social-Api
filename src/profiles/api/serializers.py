from rest_framework import serializers
from ..models import Profile, Relationship


class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    avatar = serializers.ImageField(read_only=True)
    updated = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'

    def get_updated(self, obj):
        return obj.created.strftime("%m/%d/%Y, %H:%M:%S")

    def get_created(self, obj):
        return obj.created.strftime("%m/%d/%Y, %H:%M:%S")


class ProfileAvatarSerialize(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('avatar',)


class ProfileFriendSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    avatar = serializers.ImageField(read_only=True)
    friends = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    get_friends_no = serializers.CharField()

    class Meta:
        model = Profile
        fields = '__all__'

    def get_friends(self, obj):
        for friend in obj.friends.all():
            return friend.user.username

    def get_updated(self, obj):
        return obj.created.strftime("%m/%d/%Y, %H:%M:%S")

    def get_created(self, obj):
        return obj.created.strftime("%m/%d/%Y, %H:%M:%S")
