from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient, APIRequestFactory, APISimpleTestCase

from user.models import AccountTarif, User


# client = APIClient()


# class AccountTarifTests(APISimpleTestCase):
#     url = reverse('account_tarif')
#     url_detail = reverse('account_tarif_detail', kwargs={'pk': 2})
    

#     def test_create_list_account_tarif(self):
#         # Создаем два объекта AccountTarif
#         data = {
#             'title': 'Test title',
#             'monthly_price': 100,
#             'transfer_limit': 100000,
#             'free_card_maintenance': True,
#             'additional_interest_rate': 1.0
#         }
#         response = client.post(self.url, data, format='json')

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(AccountTarif.objects.count(), 1)
#         self.assertEqual(AccountTarif.objects.get(pk=1).title, 'Test title')
        
#         data['title'] = 'Test title 2'
#         client.post(self.url, data, format='json')
#         response = client.get(self.url)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)

#     def test_retrive_update_delete_account_tarif(self):
#         # Берем, обновляем и удаляем объект AccountTarif с pk=2
#         response = client.get(self.url_detail)
#         response = client.get(self.url).data
#         print('response ----- ', response)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['title'], 'Test title 2')

#         response = client.put(self.url_detail, {'title': 'Test title123', 'monthly_price': 111})

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(AccountTarif.objects.get(pk=2).title, 'Test title123')
#         self.assertEqual(AccountTarif.objects.get(pk=2).monthly_price, 111)

#         response = client.delete(self.url_detail)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(AccountTarif.objects.count(), 1)
    