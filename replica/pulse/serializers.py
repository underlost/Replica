from rest_framework import serializers
from .models import Entry, Draft, Media, Topic, EntryType

class MediaSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Media
        fields = ('guid', 'user', 'title', 'description', 'pub_date', 'image', 'thumbnail', 'url')

class EntrytypeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    api_url = serializers.HyperlinkedIdentityField(view_name='Site-API:entrytype-detail', lookup_field='slug')

    class Meta:
        model = EntryType
        fields = ('guid', 'user', 'title', 'slug', 'api_url')

class TopicSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    api_url = serializers.HyperlinkedIdentityField(view_name='Site-API:topic-detail', lookup_field='slug')

    class Meta:
        model = Topic
        fields = ('guid', 'user', 'title', 'slug', 'description', 'image', 'thumbnail', 'api_url' )

class EntrySerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    topic = TopicSerializer(many=True, required=False)
    post_type = EntrytypeSerializer(many=False, required=False)
    image = MediaSerializer(many=False, required=False)
    api_url = serializers.HyperlinkedIdentityField(view_name='Site-API:entry-detail', lookup_field='guid')

    class Meta:
        model = Entry
        fields = ('title', 'slug', 'url', 'user', 'topic', 'pub_date', 'is_active', 'post_type',
        'content_format', 'deck', 'deck_html', 'body', 'body_html', 'image', 'guid', 'api_url')
