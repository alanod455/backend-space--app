from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.conf import settings

from .models import Session, Space, Task
from .serializers import SessionSerializer, SpaceSerializer, TaskSerializer, UserSerializer 

import base64
import os


class Home(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({'message': 'Welcome to your space!'})


class SessionsIndex(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SessionSerializer

    def get(self, request):
        sessions = Session.objects.filter(user=request.user)
        serializer = self.serializer_class(sessions, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id

        if not data.get('image'):
            default_path = os.path.join(settings.BASE_DIR, 'frontend', 'public', 'CARD.png')
            with open(default_path, 'rb') as f:
                encoded = base64.b64encode(f.read()).decode('utf-8')
                data['image'] = f'data:image/png;base64,{encoded}'

        try:
            data['duration'] = int(data['duration'])
        except ValueError:
            return Response({'error': 'Invalid duration value'}, status=status.HTTP_400_BAD_REQUEST)
        print("Incoming session data:", data)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SessionDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SessionSerializer

    def get(self, request, session_id):
        session = get_object_or_404(Session, id=session_id, user=request.user)
        serializer = self.serializer_class(session)
        return Response(serializer.data)

    def put(self, request, session_id):
        session = get_object_or_404(Session, id=session_id, user=request.user)
        data = request.data.copy()
        data['user'] = request.user.id

        serializer = self.serializer_class(session, data=data, partial=True)
        if serializer.is_valid():
             serializer.save()
             return Response(serializer.data)
        print("Validation errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, session_id):
        session = get_object_or_404(Session, id=session_id, user=request.user)
        session.delete()
        return Response({'success': True})


class SpacesIndex(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, session_id):
        spaces = Space.objects.filter(session_id=session_id, session__user=request.user)
        serializer = SpaceSerializer(spaces, many=True)
        return Response(serializer.data)


class TasksIndex(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskSerializer

    def get(self, request, session_id):
        tasks = Task.objects.filter(session_id=session_id, session__user=request.user)
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, session_id):
        session = get_object_or_404(Session, id=session_id, user=request.user)
        data = request.data.copy()
        data['session'] = session.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskSerializer

    def put(self, request, session_id, task_id):
        task = get_object_or_404(Task, id=task_id, session_id=session_id, session__user=request.user)
        serializer = self.serializer_class(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, session_id, task_id):
        task = get_object_or_404(Task, id=task_id, session_id=session_id, session__user=request.user)
        task.delete()
        return Response({'message': 'Task deleted'}, status=status.HTTP_200_OK)



class CreateUserView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }
            return Response(data)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    try:
      user = User.objects.get(username=request.user.username)
      try:
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh),'access': str(refresh.access_token),'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
      except Exception as token_error:
        return Response({"detail": "Failed to generate token.", "error": str(token_error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as err:
      return Response({"detail": "Unexpected error occurred.", "error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
