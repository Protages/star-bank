from django.db import transaction
from django.contrib.auth import get_user_model

from rest_framework import status
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
from .response import Response


USER_MODEL = get_user_model()


class BankAccountListCreateAPI(ListModelMixin, GenericAPIView):
    queryset = BankAccount.objects.all().select_related('user')
    serializer_class = serializers.BankAccountSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BankAccountRetriveUpdateDeleteAPI(RetrieveModelMixin,
                                        UpdateModelMixin,
                                        DestroyModelMixin,
                                        GenericAPIView):
    queryset = BankAccount.objects.all().select_related('user')
    serializer_class = serializers.BankAccountCreateUpdateSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.BankAccountSerializer(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, partial=True, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        related_obj = instance.get_related_card_or_deposit()
        with transaction.atomic():
            related_obj.delete()
            instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


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
        return self.update(request, partial=True, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


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
        return self.update(request, partial=True, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


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
        return self.update(request, partial=True, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CardTypeListCreateAPI(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = CardType.objects.all()
    serializer_class = serializers.CardTypeCreateUpdateSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.CardTypeSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = serializers.CardTypeSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CardTypeRetriveUpdateDeleteAPI(RetrieveModelMixin,
                                     UpdateModelMixin,
                                     DestroyModelMixin,
                                     GenericAPIView):
    queryset = CardType.objects.all()
    serializer_class = serializers.CardTypeCreateUpdateSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.CardTypeSerializer(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, partial=True, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CardDesignListCreateAPI(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = CardDesign.objects.all()
    serializer_class = serializers.CardDesignSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CardDesignRetriveUpdateDeleteAPI(RetrieveModelMixin,
                                       UpdateModelMixin,
                                       DestroyModelMixin,
                                       GenericAPIView):
    queryset = CardDesign.objects.all()
    serializer_class = serializers.CardDesignSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, partial=True, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CardListCreateAPI(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Card.objects.all().select_related(
        'bank_account', 'card_type', 'design'
    ).prefetch_related('card_type__cashbacks')
    serializer_class = serializers.CardCreateUpdateSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.CardSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = serializers.CardSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CardRetriveUpdateDeleteAPI(RetrieveModelMixin,
                                 UpdateModelMixin,
                                 DestroyModelMixin,
                                 GenericAPIView):
    queryset = Card.objects.all()
    serializer_class = serializers.CardCreateUpdateSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.CardSerializer(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, partial=True, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        bank_account = instance.bank_account
        with transaction.atomic():
            instance.delete()
            bank_account.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class DepositListCreateAPI(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Deposit.objects.all().select_related('bank_account')
    serializer_class = serializers.DepositCreateUpdateSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.DepositSeializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = serializers.DepositSeializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DepositRetriveUpdateDeleteAPI(RetrieveModelMixin,
                                    UpdateModelMixin,
                                    DestroyModelMixin,
                                    GenericAPIView):
    queryset = Deposit.objects.all()
    serializer_class = serializers.DepositCreateUpdateSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.DepositSeializer(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update(request, partial=True, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        bank_account = instance.bank_account
        with transaction.atomic():
            instance.delete()
            bank_account.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


# Api views for user's transactions, cards, deposits
class UserTransactionListAPI(ListModelMixin, GenericAPIView):
    serializer_class = serializers.TransactionSerializer

    def get(self, request, user_pk=None, *args, **kwargs):
        if user_pk is None:
            user = request.user
        elif user_pk == request.user.pk:
            user = request.user
        else:
            try:
                user = USER_MODEL.objects.get(pk=user_pk)
            except:
                return Response(
                    {'non_field_errors': 'Передан неверный id пользователя.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        queryset_outgoing, queryset_incoming = self.filter_queryset(
            self.get_queryset(user)
        )

        serializer_outgoing = self.get_serializer(queryset_outgoing, many=True)
        serializer_incoming = self.get_serializer(queryset_incoming, many=True)

        return Response({
            'transaction_outgoing': serializer_outgoing.data,
            'transaction_incoming': serializer_incoming.data
        })

    def get_queryset(self, user=None):
        if user is None:
            return None

        transaction_outgoing = []
        transaction_incoming = []
        bank_accounts = user.bankaccount_set.all().prefetch_related(
            'transaction_from', 'transaction_from__transaction_type',
            'transaction_from__from_number', 'transaction_from__to_number',
            'transaction_to', 'transaction_to__transaction_type',
            'transaction_to__from_number', 'transaction_to__to_number'
        )
        for bank_account in bank_accounts:
            transaction_outgoing += list(bank_account.transaction_from.all())
            transaction_incoming += list(bank_account.transaction_to.all())

        return transaction_outgoing, transaction_incoming


class UserCardListAPI(ListModelMixin, GenericAPIView):
    serializer_class = serializers.CardSerializer

    def get(self, request, user_pk=None, *args, **kwargs):
        if user_pk is None:
            user = request.user
        else:
            try:
                user = USER_MODEL.objects.get(pk=user_pk)
            except:
                return Response(
                    {'non_field_errors': 'Передан неверный id пользователя.'},
                    status=status.HTTP_404_NOT_FOUND
                )

        queryset = self.filter_queryset(self.get_queryset(user))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self, user=None):
        return Card.objects.filter(bank_account__user=user).select_related(
            'bank_account', 'card_type', 'design'
        ).prefetch_related('card_type__cashbacks')


class UserDepositListAPI(UserCardListAPI):
    serializer_class = serializers.DepositSeializer

    def get_queryset(self, user=None):
        return Deposit.objects.filter(
            bank_account__user=user
        ).select_related('bank_account')
