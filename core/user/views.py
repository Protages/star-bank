from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import User, AccountTarif
from .serializers import UserSerializer, AccountTarifSerializer
from .permissions import IsSuperuserOrOwner


class UsersCreateListAPI(APIView):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        queryset = User.objects.all().select_related('tarif')
        serializer = UserSerializer(queryset, many=True, context={'request': request})

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class UserUpdateRetriveAPI(APIView):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        seriaizer = UserSerializer(user, data=request.data, partial=True)
        seriaizer.is_valid(raise_exception=True)
        seriaizer.save()

        return Response(seriaizer.data)

    def delete(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response({'message': 'Пользователь был удален.'})


class AccountTarifListCreateAPI(APIView):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        queryset = AccountTarif.objects.all()
        serializer = AccountTarifSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = AccountTarifSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AccountTarifUpdateRetriveAPI(APIView):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk, *args, **kwargs):
        account_tarif = get_object_or_404(AccountTarif, pk=pk)
        serializer = AccountTarifSerializer(account_tarif)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        account_tarif = get_object_or_404(AccountTarif, pk=pk)
        serializer = AccountTarifSerializer(account_tarif, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
