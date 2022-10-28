from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)
from rest_framework.generics import GenericAPIView

from bank.response import Response
from .models import User, AccountTarif
from . import serializers


class UsersListCreateAPI(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = User.objects.all().prefetch_related('tarif')
    serializer_class = serializers.UserCreateUpdateSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = serializers.UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserRetriveUpdateDeleteAPI(RetrieveModelMixin,
                                 UpdateModelMixin,
                                 DestroyModelMixin,
                                 GenericAPIView):
    queryset = User.objects.all().select_related('tarif')
    serializer_class = serializers.UserCreateUpdateSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.UserSerializer(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, partial=True, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class AccountTarifListCreateAPI(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = AccountTarif.objects.all()
    serializer_class = serializers.AccountTarifSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AccountTarifRetriveUpdateDeleteAPI(RetrieveModelMixin,
                                         UpdateModelMixin,
                                         DestroyModelMixin,
                                         GenericAPIView):
    queryset = AccountTarif.objects.all()
    serializer_class = serializers.AccountTarifSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, partial=True, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
