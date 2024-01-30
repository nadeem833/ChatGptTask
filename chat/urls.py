from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import register, login , chat , logout

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('user/register/', register, name='register'),  
    path('user/login/', login, name='login'), 
    path('user/logout/', logout, name='logout'), 
    path('user/chat/', chat, name='chat'),
]
