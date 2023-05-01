import jwt
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from typing import Optional, Tuple, Any

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from users.models import User


class TrustMeBroAuthentication(BaseAuthentication):
    def authenticate(self, request) -> Optional[Tuple[AbstractUser, Any]]:
        """
        User 찾으면 user 반환, 그 외에는 None(필수) 반환
        :param request:
        :return:
        """
        username = request.headers.get('Trust-Me')
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
            return user, None
        except User.DoesNotExist:
            raise AuthenticationFailed(f"No user {username}")


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request) -> Optional[Tuple[AbstractUser, Any]]:
        token = request.headers.get("Authorization")
        if not token:
            return None
        decoded_content = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
        )
        pk = decoded_content.get('pk')
        if not pk:
            raise AuthenticationFailed("Invalid Token")
        try:
            user = User.objects.get(pk=pk)
            return user, None
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")
