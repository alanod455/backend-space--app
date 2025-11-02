from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Session, Space, Task
from .serializers import SpaceSerializer, TaskSerializer
from .serializers import SessionSerializer
from django.shortcuts import get_object_or_404

import base64
import os
from django.conf import settings

class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to your space!'}
    return Response(content)



class SessionsIndex(APIView):
    serializer_class = SessionSerializer

    def get(self, request):
        try:
            queryset = Session.objects.all()
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            print("Line 28 Received data:", request.data)
            data = request.data.copy()

            if not data.get('image'):
                default_path = os.path.join(settings.BASE_DIR, 'frontend', 'public', 'CARD.png')
                with open(default_path, 'rb') as f:
                    encoded = base64.b64encode(f.read()).decode('utf-8')
                    data['image'] = f'data:image/png;base64,{encoded}'

            if 'duration' in data:
                try:
                    data['duration'] = int(data['duration'])
                except ValueError:
                    return Response({'error': 'Invalid duration value'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            import traceback
            traceback.print_exc()
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
class  SessionDetail(APIView):
  serializer_class =  SessionSerializer
  lookup_field = 'id'

  def get(self, request,  session_id):
    try:
        queryset = Session.objects.get(id=session_id)  
        session = SessionSerializer(queryset)
        return Response(session.data, status=status.HTTP_200_OK)
    except Exception as err:
        return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

  def put(self, request, session_id):
    try: 
        session = get_object_or_404(Session, id=session_id)
        serializer = self.serializer_class(session, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as err:
        return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

  def delete(self, request, session_id):
    try:
        session = get_object_or_404(Session, id=session_id)
        session.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)
    except Exception as err:
        return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SpacesIndex(APIView):
    def get(self, request, session_id):
        spaces = Space.objects.filter(session_id=session_id)
        serializer = SpaceSerializer(spaces, many=True)
        return Response(serializer.data)



class TasksIndex(APIView):
  serializer_class = TaskSerializer

  def get(self, request, session_id):
    try:
      queryset = Task.objects.filter(session_id=session_id)
      return Response(self.serializer_class(queryset, many=True).data, status=status.HTTP_200_OK)
    except Exception as err:
      return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


  def post(self, request, session_id):
        try:
            session = Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['session'] = session.id
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetail(APIView):
    serializer_class = TaskSerializer

    def put(self, request, session_id, task_id):
        try:
            task = Task.objects.get(id=task_id, session_id=session_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, session_id, task_id):
        try:
            task = Task.objects.get(id=task_id, session_id=session_id)
            task.delete()
            return Response({'message': 'Task deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)