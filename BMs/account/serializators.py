from rest_framework import serializers

from django.contrib.auth.models import User

class FollowersSerializator(serializers.Serializer):

    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('followers_count')

    def get_followers_count(self, obj):
        return obj.followers.all().count()
