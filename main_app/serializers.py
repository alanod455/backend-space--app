from rest_framework import serializers
from .models import Session,Space

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'title', 'duration', 'image', 'sound', 'created_at']

        extra_kwargs = {
            'image': {'required': False, 'allow_null': True},
            'duration': {'required': False, 'allow_null': True},
            'sound': {'required': False, 'allow_null': True}
        }

class SpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = '__all__'
        read_only_fields = ['type'] 

    def create(self, validated_data):
        session = validated_data['session']
        duration = session.duration

        if duration is None:
            space_type = 'star'  
        elif duration <= 30:
            space_type = 'star'
        else:
            space_type = 'planet'

        validated_data['type'] = space_type
        return super().create(validated_data)
