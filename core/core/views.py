from django.urls import reverse
from django.shortcuts import redirect

from rest_framework.response import Response
from rest_framework.views import APIView


def redirect_to_root(request):
    return redirect('root')


class RootAPI(APIView):
    def get(self, request, *args, **kwargs):
        api_mapping = {
            'swagger-ui': self.get_full_url('swagger-ui'),
            'user': self.get_full_url('user'),
            'account_tarif': self.get_full_url('account_tarif'),
            'bank_account': self.get_full_url('bank_account'),
            'transaction_type': self.get_full_url('transaction_type'),
            'transaction': self.get_full_url('transaction'),
            'cashback': self.get_full_url('cashback'),
            'card_type': self.get_full_url('card_type'),
            'card_design': self.get_full_url('card_design'),
            'card': self.get_full_url('card'),
            'deposit': self.get_full_url('deposit'),
            'my_transaction': self.get_full_url('my_transaction'),
            'user_transaction': self.get_full_url('user_transaction', user_pk=1),
            'my_card': self.get_full_url('my_card'),
            'user_card': self.get_full_url('user_card', user_pk=1),
            'my_deposit': self.get_full_url('my_deposit'),
            'user_deposit': self.get_full_url('user_deposit', user_pk=1),
        }
        return Response(api_mapping)

    def get_full_url(self, url_name, **kwargs):
        host = self.request.get_host()
        scheme = self.request.scheme
        url = reverse(url_name, kwargs={**kwargs})
        return f'{scheme}://{host}{url}'
