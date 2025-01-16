from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('api/register/user', views.RegisterStudents.as_view(), name='register_user'),
    path('api/login/user', views.LoginStudent.as_view(), name='login_user'),
    path('api/details/user', views.UserDetailView.as_view(), name='user_detail'),
    path('api/update/user', views.UpdateUserView.as_view(), name='update_user'),
    path('api/refresh/token/user',views.TokenRefreshView.as_view(),name='refresh_token'),
    path('api/logout/user',views.LogoutView.as_view(),name='logout_user'),
]
