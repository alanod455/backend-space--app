from django.urls import path
from .views import Home, SessionsIndex, SessionDetail

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('sessions/', SessionsIndex.as_view()),
  path('sessions/<int:session_id>/', SessionDetail.as_view()),
]
