import json
from django.test import TestCase, Client
from django.core.management import call_command

from products.models import *

# Create your tests here.
class CarrierTestCase(TestCase):
    fixtures = ['fixtures/initial_data.json',]

    def create_data(self, state, zipcode, product_types, quantity):
        items = []
        for idx, product_type in enumerate(product_types):
            variant = Variant.objects.filter(
                product__product_type__title=product_type).order_by('?').first()
            items.append({
                'variant_id': variant.shopify_id,
                'quantity': quantity[idx],
                'price': float(variant.price),
            })
        return json.dumps({
           "rate": {
               "origin": {
                   "country": "CA",
                   "postal_code": "K1S4J3",
                   "province": "ON",
                   "city": "Ottawa",
                   "name": None,
                   "address1": "520 Cambridge Street South",
                   "address2": None,
                   "address3": None,
                   "phone": None,
                   "fax": None,
                   "address_type": None,
                   "company_name": None
               },
               "destination": {
                   "country": "USA",
                   "postal_code": zipcode,
                   "province": state,
                   "city": "Ottawa",
                   "name": "Jason Normore",
                   "address1": "520 Cambridge Street South Apt. 5",
                   "address2": None,
                   "address3": None,
                   "phone": "7097433959",
                   "fax": None,
                   "address_type": None,
                   "company_name": None
               },
               "items": items,
               "currency": "CAD"
           }
        })

    def create_product_data(self, state, zipcode, variants):
        items = []
        for variant in variants:
            items.append({
                'variant_id': variant.shopify_id,
                'quantity': 1,
                'price': float(variant.price),
            })
        return json.dumps({
           "rate": {
               "origin": {
                   "country": "CA",
                   "postal_code": "K1S4J3",
                   "province": "ON",
                   "city": "Ottawa",
                   "name": None,
                   "address1": "520 Cambridge Street South",
                   "address2": None,
                   "address3": None,
                   "phone": None,
                   "fax": None,
                   "address_type": None,
                   "company_name": None
               },
               "destination": {
                   "country": "USA",
                   "postal_code": zipcode,
                   "province": state,
                   "city": "Ottawa",
                   "name": "Jason Normore",
                   "address1": "520 Cambridge Street South Apt. 5",
                   "address2": None,
                   "address3": None,
                   "phone": "7097433959",
                   "fax": None,
                   "address_type": None,
                   "company_name": None
               },
               "items": items,
               "currency": "CAD"
           }
        })

    def testNewYork(self):
        c = Client()
        # One Sectional 11999
        data = self.create_data('NY', '10030', ['sectionals'], [1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 11999)
        # One Sectional One Ottoman 15998
        data = self.create_data('NY', '10038', ['sectionals', 'rugs'], [1, 1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 15998)
        # One Sofa 9999
        data = self.create_data('NY', '10001', ['sofas'], [1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 9999)
        # Two Sofas 19998
        data = self.create_data('NY', '10016', ['sofas'], [2])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 19998)
        # Three Sofas 19999
        data = self.create_data('NY', '10033', ['sofas'], [3])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 19999)
        # Sofa and Lamp
        data = self.create_data('NY', '10026', ['sofas', 'ottomans'], [1, 1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 13998)
        # Recliners
        data = self.create_data('NY', '10045', ['recliners'], [1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 8999)
        data = self.create_data('NY', '10125', ['recliners'], [2])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 9999)
        # Chairs
        data = self.create_data('NY', '10213', ['accent chairs'], [1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 8999)
        data = self.create_data('NY', '10453', ['accent chairs'], [2])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 9999)
        # Bed
        data = self.create_data('NY', '10302', ['beds'], [1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 8999)
        # Mattresses
        data = self.create_data('NY', '11412', ['mattresses'], [1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 7999)

    def testNewYorkPlus(self):
        c = Client()
        # Shelter Island One Sectional 11999
        data = self.create_data('NY', '11964', ['sectionals'], [1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 19499)
        # Ulster One Sectional One Ottoman 15998
        data = self.create_data('NY', '12401', ['sectionals', 'rugs'], [1, 1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 23498)
        # Orange One Sofa 9999
        data = self.create_data('NY', '10910', ['sofas'], [1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 11999)
        # Columbia Two Sofas 19998
        data = self.create_data('NY', '12050', ['sofas'], [2])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 27498)
        # Sullivan Three Sofas 19999
        data = self.create_data('NY', '12701', ['sofas'], [3])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 27499)
        # Ulster Sofa and Lamp
        data = self.create_data('NY', '12404', ['sofas', 'ottomans'], [1, 1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 21498)
        # Orange Recliners
        data = self.create_data('NY', '10912', ['recliners'], [1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 10999)
        data = self.create_data('NY', '10953', ['recliners'], [2])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 11999)
        # Columbia Chairs
        data = self.create_data('NY', '12516', ['accent chairs'], [1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 16499)
        data = self.create_data('NY', '12172', ['accent chairs'], [2])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 17499)
        # Sullivan Bed
        data = self.create_data('NY', '12747', ['beds'], [1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 16499)
        # Sullivan Mattresses
        data = self.create_data('NY', '12783', ['mattresses'], [1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 15499)

    def testNewJersey(self):
        c = Client()
        # Somerset One Sectional 11999
        data = self.create_data('NJ', '07059', ['sectionals'], [1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 11999)
        # Monmouth One Sectional One Ottoman 15998
        data = self.create_data('NJ', '07717', ['sectionals', 'rugs'], [1, 1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 15998)
        # Bergen One Sofa 9999
        data = self.create_data('NJ', '07071', ['sofas'], [1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 9999)
        # Morris Two Sofas 19998
        data = self.create_data('NJ', '07801', ['sofas'], [2])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 19998)
        # Passaic Three Sofas 19999
        data = self.create_data('NJ', '07474', ['sofas'], [3])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 19999)
        # Union Sofa and Lamp
        data = self.create_data('NJ', '07088', ['sofas', 'ottomans'], [1, 1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 13998)
        # Hudson & Ocean Recliners
        data = self.create_data('NJ', '07096', ['recliners'], [1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 8999)
        data = self.create_data('NJ', '08527', ['recliners'], [2])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 9999)
        # Mercer, Cape May Chairs
        data = self.create_data('NJ', '08450', ['accent chairs'], [1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 8999)
        data = self.create_data('NJ', '08242', ['accent chairs'], [2])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 9999)
        # Bed
        data = self.create_data('NJ', '08557', ['beds'], [1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 8999)
        # Mattresses
        data = self.create_data('NJ', '07825', ['mattresses'], [1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 7999)

    def testCT(self):
        c = Client()
        # Fairfield One Sectional 11999
        data = self.create_data('CT', '06804', ['sectionals'], [1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 11999)
        # New Haven One Sectional One Ottoman 15998
        data = self.create_data('CT', '06451', ['sectionals', 'rugs'], [1, 1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 15998)
        # Hartford One Sofa 9999
        data = self.create_data('CT', '06020', ['sofas'], [1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 19999)
        # Litchfield Two Sofas 19998
        data = self.create_data('CT', '06426', ['sofas'], [2])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 19998)
        # Monroe Three Sofas 19999
        data = self.create_data('PA', '18350', ['sofas'], [3])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 27499)
        # Northhampton Sofa and Lamp
        data = self.create_data('PA', '18064', ['sofas', 'ottomans'], [1, 1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 21498)
        # Philadephia Recliners
        data = self.create_data('PA', '19019', ['recliners'], [1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 10999)
        data = self.create_data('PA', '19125', ['recliners'], [2])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 11999)
        # Farfield Chairs
        data = self.create_data('CT', '06825', ['accent chairs'], [1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 8999)
        data = self.create_data('CT', '06532', ['accent chairs'], [2])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 9999)
        # Litchfield Bed
        data = self.create_data('CT', '06759', ['beds'], [1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 16499)
        # Pike Mattresses
        data = self.create_data('PA', '18324', ['mattresses'], [1])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], 15499)

    def testLODESTAR(self):
        c = Client()
        variant = Variant.objects.filter(
            product__product_type__title="bedroom sets", price__gt=2000).first()
        # Sussex One Sectional 11999
        price = int(variant.price * 100) * 0.05
        if price < 14999:
            price = 14999
        price += variant.pieces * 500
        data = self.create_product_data('DE', '19930', [variant])
        response = c.post('/webhooks/carrier/', data, content_type="application/json")
        self.assertEqual(response.json()['rates'][0]['service_name'], "Local Delivery")
        self.assertEqual(response.json()['rates'][0]['total_price'], price)
