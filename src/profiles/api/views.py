from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from profiles.models import Profile, Relationship
from .serializers import ProfileSerializer, ProfileFriendSerializer, RelationshipSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework import status, viewsets
from django.contrib.auth.models import User
import json


class ProfileList(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]


class ProfileDetail(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]


class Profiles5List(ListAPIView):
    serializer_class = ProfileFriendSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.id
        queryset = Profile.objects.get_people_to_invite(user)
        return queryset


class ProfileFriendsList(ListAPIView):
    serializer_class = ProfileFriendSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        queryset = profile.get_friends
        return queryset


@api_view(['GET'])
def user_info(request):
    profile = Profile.objects.get(user=request.user)
    serializer = ProfileSerializer(profile)
    return Response(serializer.data)


@api_view(['GET'])
def my_invations_received(request, *args, **kwargs):
    rec = request.user.id
    profile = Profile.objects.get(user=request.user)
    profiles = Profile.objects.all()
    rel = Relationship.objects.invations_received(rec)
    invites = [x for x in rel if x.receiver.id ==
               profile.id and x.status == 'send']
    result = map(lambda x: x.sender, invites)
    serializer = ProfileSerializer(result, many=True)
    return Response(serializer.data)


class RelationshipViewset(viewsets.ModelViewSet):
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def accept_invatation(self, request, pk=None, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        receiver = self.request.user.id
        user = User.objects.get(id=pk)
        sender = Profile.objects.get(id=user.id)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
        serializer = RelationshipSerializer(rel)
        response = {
            'works': 'yes',
            'rel': serializer.data
        }
        return Response(response)

    @action(detail=True, methods=['post'])
    def send_invatation(self, request, pk=None, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        sender_ = self.request.user.id
        sender = Profile.objects.get(id=sender_)
        user = User.objects.get(id=pk)
        receiver = Profile.objects.get(id=user.id)

        obj, created = Relationship.objects.get_or_create(
            sender=sender, receiver=receiver)
        obj.status = 'send'
        obj.save()
        serializer = RelationshipSerializer(obj)
        response = {
            'works': 'yes',
            'result': serializer.data
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        serializer.save(author=user, profile=profile)
