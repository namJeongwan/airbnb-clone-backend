from django.contrib.auth import authenticate, login, logout
from django.conf import settings

from rest_framework.exceptions import ParseError, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

import jwt

from .models import User
from .serializers import TinyUserSerializer, PrivateUserSerializer, PublicUserSerializer


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(PrivateUserSerializer(user).data)

    def put(self, request):
        user = request.user
        serializer = PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_user = serializer.save()
            serializer = PrivateUserSerializer(updated_user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Users(APIView):
    def post(self, request):
        password = request.data.get('password')
        if not password:
            raise ParseError("Password is required")
        serializer = PrivateUserSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            new_user = serializer.save()
            new_user.set_password(password)
            new_user.save()
            serializer = PrivateUserSerializer(new_user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PublicUser(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            serializer = PublicUserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            raise NotFound()


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        cur_password = request.data.get('cur-password')
        new_password = request.data.get('new-password')

        if not cur_password or not new_password:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if user.check_password(cur_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogIn(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            raise ParseError("ID, Password is required..")
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"result": "S"})
        else:
            return Response({"error": "wrong password or id"})


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"result": "bye"})


class JWTLogIn(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            raise ParseError("ID, Password is required..")
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({'token': token})
        else:
            return Response({"error": "wrong password or id"})