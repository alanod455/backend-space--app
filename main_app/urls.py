from django.urls import path
from .views import Home, SessionsIndex, SessionDetail,SpacesIndex, TasksIndex, TaskDetail, CreateUserView, LoginView,VerifyUserView

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('sessions/', SessionsIndex.as_view()),
  path('sessions/<int:session_id>/', SessionDetail.as_view()),
  path('sessions/<int:session_id>/spaces/', SpacesIndex.as_view()),
  path('sessions/<int:session_id>/tasks/', TasksIndex.as_view()),
  path('sessions/<int:session_id>/tasks/<int:task_id>/', TaskDetail.as_view()),
  path('users/signup/', CreateUserView.as_view()),
  path('users/login/', LoginView.as_view(), name='login'),
  path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),

]
