from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.views import UserDetailsView, LoginView, PasswordChangeView
from django.urls import path
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenVerifyView

user_details_view = extend_schema(tags=["Authentication"])(UserDetailsView)
login_view = extend_schema(tags=["Authentication"])(LoginView)
password_change_view = extend_schema(tags=["Authentication"])(PasswordChangeView)
refresh_view = extend_schema(tags=["Authentication"])(get_refresh_view())
token_verify_view = extend_schema(tags=["Authentication"])(TokenVerifyView)

urlpatterns = [
    path('login/', login_view.as_view(), name='rest_login'),
    path('user/', user_details_view.as_view(), name='rest_user_details'),
    path('password/change/', password_change_view.as_view(), name='rest_password_change'),
    path('token/verify/', token_verify_view.as_view(), name='token_verify'),
    path('token/refresh/', refresh_view.as_view(), name='token_refresh')
]
