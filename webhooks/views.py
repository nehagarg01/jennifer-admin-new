from django.shortcuts import render
from shopify_webhook.views  import WebhookView


class ShopifyWebhookView(WebhookView):

    def post(self, request, *args, **kwargs):
        response = super(ShopifyWebhookView, self).post(request, *args, **kwargs)
        from core.celery import add
        add.delay(4,4)
        print request.webhook_topic
        return response


class ShopifyWebhookProductUpdate(WebhookView):

    def post(self, request, *args, **kwargs):
        response = super(ShopifyWebhookProductUpdate, self).post(request, *args, **kwargs)
        from products.utils import shopify
        from products.models import Product
        shopify_product = shopify.Product.find(request.webhook_data['id'])
        Product.shopify_sync(shopify_product)
        return response
