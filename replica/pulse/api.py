from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from coreExtend.models import Account as User
from replica.api.permissions import IsOwnerPermission, IsOwnerOrReadOnly

from .models import Entry, Draft, Media, Topic, EntryType
from .serializers import *

class TopicDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = Topic.objects.public()
    serializer_class = TopicSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class EntryTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    queryset = EntryType.objects.all()
    serializer_class = EntrytypeSerializer
    permission_classes = (IsOwnerOrReadOnly,)

class TopicList(generics.ListAPIView):
    lookup_field = 'slug'
    serializer_class = TopicSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            request_user = self.request.user
            topics = Topic.objects.filter(
                Q(is_public=True) |
                Q(user__username=request_user.username)
            )
            return topics
        else:
            return Topic.objects.filter(is_public=True)

class TopicEntryList(generics.ListAPIView):
    model = Entry
    serializer_class = EntrySerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            request_user = self.request.user
            entries = Entry.objects.posts().filter(
                Q(is_active=True) |
                Q(user__username=request_user.username)
            )
            return entries.filter(topic__slug=self.kwargs.get('slug'))
        else:
            return Entry.objects.published().filter(topic__slug=self.kwargs.get('slug'))

class EntryList(generics.ListAPIView):
    model = Entry
    serializer_class = EntrySerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            request_user = self.request.user
            entries = Entry.objects.posts().filter(
                Q(is_active=True) |
                Q(user__username=request_user.username)
            )
            return entries
        else:
            return Entry.objects.published()

class EntryTypeList(generics.ListAPIView):
    lookup_field = 'slug'
    serializer_class = EntrytypeSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        return EntryType.objects.all()

class EntryTypeEntryList(generics.ListAPIView):
    model = Entry
    serializer_class = EntrySerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            request_user = self.request.user
            entries = Entry.objects.posts().filter(
                Q(is_active=True) |
                Q(user__username=request_user.username)
            )
            return entries.filter(post_type__slug=self.kwargs.get('slug'))
        else:
            return Entry.objects.published().filter(post_type__slug=self.kwargs.get('slug'))

class EntryDraftList(generics.ListAPIView):
    model = Entry
    serializer_class = EntrySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        request_user = self.request.user
        entries = Entry.objects.ideas().filter(user__username=request_user.username)
        return entries

class EntryUpcomingList(generics.ListAPIView):
    model = Entry
    serializer_class = EntrySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        request_user = self.request.user
        entries = Entry.objects.upcoming().filter(user__username=request_user.username)
        return entries

class EntryDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'guid'
    queryset = Entry.objects.published()
    serializer_class = EntrySerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def pre_save(self, obj):
        """Force user to the current user on save"""
        obj.user = self.request.user
        return super(EntryDetail, self).pre_save(obj)


class PageList(generics.ListAPIView):
    model = Entry
    serializer_class = EntrySerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            request_user = self.request.user
            entries = Entry.objects.pages().filter(
                Q(is_active=True) |
                Q(user__username=request_user.username)
            )
            return entries
        else:
            return Entry.objects.published_pages()

class PageDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'guid'
    queryset = Entry.objects.published_pages()
    serializer_class = EntrySerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def pre_save(self, obj):
        """Force user to the current user on save"""
        obj.user = self.request.user
        return super(PagesDetail, self).pre_save(obj)
