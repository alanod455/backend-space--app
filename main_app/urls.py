from django.urls import path
from .views import Home, SessionsIndex, SessionDetail,SpacesIndex

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('sessions/', SessionsIndex.as_view()),
  path('sessions/<int:session_id>/', SessionDetail.as_view()),
  path('sessions/<int:session_id>/spaces/', SpacesIndex.as_view()),

]
