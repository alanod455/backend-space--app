from rest_framework import serializers
from .models import Session,Space,Task
from django.contrib.auth.models import User

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



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'duration', 'session', 'created_at']
        
        
        
class SessionSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Session
        fields = ['id', 'title', 'duration', 'image', 'sound', 'created_at', 'tasks', 'user']
        extra_kwargs = {
            'image': {'required': False, 'allow_null': True},
            'duration': {'required': False, 'allow_null': True},
            'sound': {'required': False, 'allow_null': True}
        }



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']  
        )
      
        return user