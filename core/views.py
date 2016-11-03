import json
import googlemaps

from django.views.generic import ListView, View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


class SearchView(ListView):

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['form'] = self.search_form(self.request.GET or None, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        queryset = super(SearchView, self).get_queryset()
        form = self.search_form(self.request.GET or None, queryset=queryset)
        if form.is_valid():
            queryset = form.search()
        return queryset


@csrf_exempt
def carrier_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)['rate']
        state = data['destination']['province']
        zipcode = data['destination']['postal_code']

        gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
        response = gmaps.geocode("%s %s USA" % (state, zipcode))
        if len(response):
            loc = response[0]
            county = ''
            for obj in loc['address_components']:
                if "administrative_area_level_2" in obj['types']:
                    county = obj['long_name']
            print county
        items = data['items']
        return JsonResponse({
           "rates": [
               {
                   "service_name": "canadapost-overnight",
                   "service_code": "ON",
                   "total_price": "1295",
                   "description": "This is the fastest option by far",
                   "currency": "CAD",
                   "min_delivery_date": "2013-04-12 14:48:45 -0400",
                   "max_delivery_date": "2013-04-12 14:48:45 -0400"
               },
               {
                   "service_name": "fedex-2dayground",
                   "service_code": "2D",
                   "total_price": "2934",
                   "currency": "USD",
                   "min_delivery_date": "2013-04-12 14:48:45 -0400",
                   "max_delivery_date": "2013-04-12 14:48:45 -0400"
               },
               {
                   "service_name": "fedex-priorityovernight",
                   "service_code": "1D",
                   "total_price": "3587",
                   "currency": "USD",
                   "min_delivery_date": "2013-04-12 14:48:45 -0400",
                   "max_delivery_date": "2013-04-12 14:48:45 -0400"
               }
           ]
        })
