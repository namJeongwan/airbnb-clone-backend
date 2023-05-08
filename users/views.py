from django.contrib.auth import authenticate, login, logout
from django.conf import settings

from rest_framework.exceptions import ParseError, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

import requests

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


class GithubLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            gh_url = (
                    f"https://github.com/login/oauth/access_token?code={code}&"
                    f"client_id=57c19b04fbc0a0a972fb&"
                    f"client_secret={settings.GH_SECRET}"
                   )
            access_token = requests.post(
                url=gh_url,
                headers={
                    "Accept": "application/json",
                }
            )
            access_token = access_token.json().get('access_token')

            user_data = requests.get(
                url='https://api.github.com/user',
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_data = user_data.json()

            user_emails = requests.get(
                url='https://api.github.com/user/emails',
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_emails = user_emails.json()

            try:
                user = User.objects.get(email=user_emails[0]['email'])
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data.get('login'),
                    email=user_emails[0]['email'],
                    name=user_data.get('name'),
                    avatar=user_data.get('avatar_url'),
                )
                # 해당 User는 오직 Github 로만 로그인 할 수 있음
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class KakaoLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get('code')
            access_token = requests.post(
                url="https://kauth.kakao.com/oauth/token",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data={
                    "grant_type": "authorization_code",
                    "client_id": "c143a4c1353741c1579ad78a6d346e74",
                    "redirect_uri": "http://127.0.0.1:3000/social/kakao",
                    "code": code,
                }
            )
            access_token = access_token.json().get('access_token')
            user_data = requests.get(
                url="https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;"
                                    "charset=utf-8",
                },
            )
            user_data = user_data.json()
            kakao_account = user_data.get('kakao_account')
            profile = kakao_account.get('profile')

            try:
                user = User.objects.get(email=kakao_account.get('email'))
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                # 해당 User는 오직 Github 로만 로그인 할 수 있음
                print(profile)
                print(kakao_account)
                user = User.objects.create(
                    email=kakao_account.get('email'),
                    username=profile.get('nickname'),
                    name=profile.get('nickname'),
                    avatar=profile.get('profile_image_url'),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            print(e.with_traceback())
            return Response(status=status.HTTP_400_BAD_REQUEST)
