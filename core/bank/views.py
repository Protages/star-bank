from django.shortcuts import render, get_object_or_404
from django.db.models.query import QuerySet

from rest_framework.views import APIView, Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin, 
    CreateModelMixin, 
    RetrieveModelMixin, 
    UpdateModelMixin,
    DestroyModelMixin
)

from .models import (
    BankAccount,
    TransactionType,
    Transaction,
    Cashback,
    CardType,
    CardDesign,
    Card,
    Deposit,
)
from . import serializers


class BankAccountListCreateAPI(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = serializers.BankAccountSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BankAccountRetriveUpdateDeleteAPI(RetrieveModelMixin, 
                                        UpdateModelMixin, 
                                        DestroyModelMixin, 
                                        GenericAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = serializers.BankAccountSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class TransactionTypeListCreateAPI(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = TransactionType.objects.all()
    serializer_class = serializers.TransactionTypeSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TransactionTypeRetriveUpdateDeleteAPI(RetrieveModelMixin, 
                                        UpdateModelMixin, 
                                        DestroyModelMixin, 
                                        GenericAPIView):
    queryset = TransactionType.objects.all()
    serializer_class = serializers.TransactionTypeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class TransactionListCreateAPI(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Transaction.objects.all().select_related(
        'from_number', 'to_number', 'transaction_type'
    )
    serializer_class = serializers.TransactionCreateUpdateSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.TransactionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = serializers.TransactionSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

class TransactionRetriveUpdateDeleteAPI(RetrieveModelMixin, 
                                        UpdateModelMixin, 
                                        DestroyModelMixin, 
                                        GenericAPIView):
    queryset = Transaction.objects.all().select_related(
        'from_number', 'to_number', 'transaction_type'
    )
    serializer_class = serializers.TransactionCreateUpdateSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.TransactionSerializer(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class CashbackListCreateAPI(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Cashback.objects.all().prefetch_related('transaction_type')
    serializer_class = serializers.CashbackCreateUpdateSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.CashbackSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = serializers.CashbackSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CashbackRetriveUpdateDeleteAPI(RetrieveModelMixin, 
                              UpdateModelMixin, 
                              DestroyModelMixin, 
                              GenericAPIView):
    queryset = Cashback.objects.all().prefetch_related('transaction_type')
    serializer_class = serializers.CashbackCreateUpdateSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.CashbackSerializer(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
