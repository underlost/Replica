from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from coreExtend.models import Account as User
from replica.api.permissions import IsOwnerPermission, IsOwnerOrReadOnly

from .models import Timeline, Blip
from .serializers import *


#Lists all blips request.user has access to
class BlipList(generics.ListAPIView):
    lookup_field = 'guid'
    serializer_class = BlipSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            request_user = self.request.user
            blips = Blip.objects.filter(
                Q(is_private=False) |
                Q(user__username=request_user.username)
            )
            return blips
        else:
            return Blip.objects.filter(is_private=False)

class TimelineList(generics.ListAPIView):
    lookup_field = 'guid'
    serializer_class = TimelineSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            request_user = self.request.user
            timelines = Timeline.objects.filter(
                Q(is_public=True) |
                Q(user__username=request_user.username)
            )
            return timelines
        else:
            return Timeline.objects.filter(is_public=True)

class UserTimelineList(generics.ListAPIView):
    lookup_field = 'username'
    serializer_class = TimelineSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        request_user = self.request.user
        user = self.kwargs['username']
        if request_user.username == user:
            return Timeline.objects.filter(user__username=user)
        else:
            return Timeline.objects.filter(user__username=user).filter(is_public=True)

class UserBlipList(generics.ListAPIView):
    lookup_field = 'username'
    serializer_class = BlipSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        request_user = self.request.user
        user = self.kwargs['username']
        if request_user.username == user:
            return Blip.objects.filter(user__username=user)
        else:
            return Blip.objects.filter(user__username=user).filter(is_private=False)

class TimelineBlipList(generics.ListAPIView):
    model = Blip
    serializer_class = BlipSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            request_user = self.request.user
            blips = Blip.objects.filter(
                Q(is_private=False) |
                Q(user__username=request_user.username)
            )
            return blips.filter(timeline__slug=self.kwargs.get('slug'))
        else:
            return Blip.objects.filter(is_private=False).filter(timeline__slug=self.kwargs.get('slug'))

class BlipDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'guid'
    queryset = Blip.objects.all()
    serializer_class = BlipSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class TimelineDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = Timeline.objects.all()
    serializer_class = TimelineSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class BlipCreate(generics.CreateAPIView):
    lookup_field = 'guid'
    model = Blip
    serializer_class = BlipSerializer
    permission_classes = [ IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TimelineCreate(generics.CreateAPIView):
    lookup_field = 'slug'
    model = Timeline
    serializer_class = TimelineSerializer
    permission_classes = [ IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
