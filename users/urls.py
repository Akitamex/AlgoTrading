from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import UsersAPIView, UserAPIUpdate, ReferalAPIView, UserAPIView, RoleAPIView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', UsersAPIView.as_view()),
    path('<uuid:id>/', UserAPIUpdate.as_view(), name='user-detail'),
    path('referals/', ReferalAPIView.as_view(), name='referals-list'),
    path('id/', UserAPIView.as_view(), name='get_single_user'),
    path('roles/', RoleAPIView.as_view(), name='get_roles')
]
