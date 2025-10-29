from rest_framework import serializers
from .models import Session

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'title', 'image']
        extra_kwargs = {
            'image': {'required': False, 'allow_null': True}
        }