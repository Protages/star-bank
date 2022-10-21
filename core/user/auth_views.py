from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from django.contrib.auth import login, logout, get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from django.middleware.csrf import get_token

from rest_framework.authentication import SessionAuthentication
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token

from bank.response import Response
from .serializers import UserLoginSerializer, UserSerializer


USER_MODEL = get_user_model()


class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        try:
            token = Token.objects.get(user=user)
        except:
            return Response(
                {'non_field_errors': 'Токена для такого пользователя не найдено.'}, 
                status=status.HTTP_404_NOT_FOUND
            )

        login(request, user)

        user_serializer = UserSerializer(user)

        return Response({'token': token.key, 'user': user_serializer.data})


# API for SessionAuth
# class LoginAPIView(GenericAPIView):
#     serializer_class = UserLoginSerializer

#     def options(self, request, *args, **kwargs):
#         if self.metadata_class is None:
#             return self.http_method_not_allowed(request, *args, **kwargs)
#         data = self.metadata_class().determine_metadata(request, self)
#         return Response(data, status=status.HTTP_200_OK)

#     @method_decorator(ensure_csrf_cookie)
#     def get(self, request, *args, **kwargs):
#         data = {'get': 'Pass csrftoken save him!'}
#         return Response(data)
    
#     @method_decorator(csrf_protect)
#     def post(self, request, *args, **kwargs):
#         try:
#             user = USER_MODEL.objects.get(username=request.data.get('username'))
#             is_pass_correct = user.check_password(request.data.get('password'))
#             if is_pass_correct:
#                 login(request, user)
#             else:
#                 raise ValueError
#         except:
#             return Response({'errors': [
#                 'Пользователя с таким login или password несуществует.'
#             ]}, status=status.HTTP_400_BAD_REQUEST)

#         return Response({'succes': f'Hello! {user.username}'})


# class LogoutAPIView(GenericAPIView):
#     def get(self, request, *args, **kwargs):
#         try:
#             logout(request)
#         except:
#             return Response(
#                 {'errors': ['We cant logout this user.']}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         return Response({'success': 'User was logout!'})
