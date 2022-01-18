from django.urls import path, include

from rest_framework_simplejwt.views import TokenRefreshView


from . import views
from .views import UserAPI

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
    path('Login/', views.LogInAPIView.as_view(), name='Login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.SignUpAPIView.as_view(), name='register'),
    path('user/', UserAPI.as_view(), name='user'),


]


