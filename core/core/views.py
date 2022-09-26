from django.urls import reverse

from rest_framework.response import Response
from rest_framework.views import APIView


class RootAPI(APIView):
    def get(self, request, *args, **kwargs):
        api_mapping = {
            'user': self.get_full_url('user'),
            'account_tarif': self.get_full_url('account_tarif'),
            'bank_account': self.get_full_url('bank_account'),
            'transaction_type': self.get_full_url('transaction_type'),
            'transaction': self.get_full_url('transaction'),
            'cashback': self.get_full_url('cashback'),
        }
        return Response(api_mapping)

    def get_full_url(self, url_name):
        host = self.request.get_host()
        scheme = self.request.scheme
        url = reverse(url_name)
        return f'{scheme}://{host}{url}'
