from django.shortcuts import render
from shopify_webhook.views  import WebhookView


class ShopifyWebhookView(WebhookView):

    def post(self, request, *args, **kwargs):
        response = super(ShopifyWebhookView, self).post(request, *args, **kwargs)
        from core.celery import add
        add.delay(4,4)
        print request.webhook_topic
        return response
