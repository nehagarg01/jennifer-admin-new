import requests
import json

from django.core.management.base import BaseCommand, CommandError
from products.models import Product
from vendors.models import Vendor

class Command(BaseCommand):
    help = 'load product fixtures'

    def handle(self, *args, **options):
        api_url = "https://d8f1052bf6d5aac68ca077a5ba13c204:ab82e2d3e5a4f94c943030d1872af44d@jennifer-convertibles.myshopify.com/admin/products.json?limit=250&page="

        incomplete = True
        page = 1
        outdata = []

        while incomplete:
            response = requests.get(api_url + str(page))
            data = response.json()
            if len(data['products']):
                for product in data['products']:
                    vendor, created = Vendor.objects.get_or_create(name=product['vendor'])
                    outdata.append({
                        "model": "products.Product",
                        "fields": {
                            "title": product['title'],
                            "body_html": product['body_html'],
                            "handle": product['handle'],
                            "product_type": product['product_type'],
                            "vendor": vendor.pk,
                            "shopify-id": product['id']
                        }
                    })
                page += 1
            else:
                incomplete = False


        with open('products/fixtures/shopify-products.json', "w") as outfile:
            json.dump(outdata, outfile)

        print "Json file created"
