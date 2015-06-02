from rest_framework import serializers
from .models import Timeline, Blip

class TimelineSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    api_url = serializers.HyperlinkedIdentityField(view_name='Site-API:timeline-detail', lookup_field='slug')

    class Meta:
        model = Timeline
        fields = ('guid', 'user', 'pub_date', 'name', 'slug', 'rev_order', 'is_public', 'guid', 'api_url')

class BlipSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    timeline = TimelineSerializer(many=False, required=False)
    api_url = serializers.HyperlinkedIdentityField( view_name='Site-API:blip-detail', lookup_field='guid')

    class Meta:
        model = Blip
        fields = ('guid', 'user', 'pub_date', 'timeline', 'is_private', 'body_html', 'api_url')

class BlipCreateSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    timeline = TimelineSerializer(many=False, required=False)
    api_url = serializers.HyperlinkedIdentityField( view_name='Site-API:blip-detail', lookup_field='guid')

    class Meta:
        model = Blip
        fields = ('guid', 'user', 'pub_date', 'timeline', 'is_private', 'body', 'api_url')
