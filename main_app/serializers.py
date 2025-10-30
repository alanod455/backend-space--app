from rest_framework import serializers
from .models import Session

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'title', 'duration', 'image', 'sound', 'created_at']

        extra_kwargs = {
            'image': {'required': False, 'allow_null': True},
            'duration': {'required': False, 'allow_null': True},
            'sound': {'required': False, 'allow_null': True}
        }