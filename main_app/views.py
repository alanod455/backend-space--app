from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Session
from .serializers import SessionSerializer


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
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
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
    
