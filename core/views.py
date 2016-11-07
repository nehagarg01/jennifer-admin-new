import json
from collections import Counter
import googlemaps
from decimal import Decimal

from django.views.generic import ListView, View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from counties import *


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

NY_COUNTY = ['New York County', 'Kings County', 'Queens County', 'Roosevelt Island Zone',
             'Bronx County', 'Staten Island County', 'Nassau County', 'West Suffolk',
            'East Suffolk', 'Shelter Island', 'Rockland County', 'Westchester County',
            'Putnam County', 'Dutchess County', 'Ulster County', 'Orange County',
            'Columbia County', 'Sullivan County']


@require_POST
@csrf_exempt
def carrier_webhook(request):
    from .counties import *
    from products.models import Variant
    data = json.loads(request.body)['rate']
    state = data['destination']['province']
    zipcode = data['destination']['postal_code']
    county = ''
    cart_total = quantity = 0
    cnt = Counter()

    for item in data['items']:
        variant = Variant.objects.filter(
            shopify_id=item['variant_id']).select_related('product').first()
        p_group = variant.get_product_group()
        if p_group not in ['protection plans', 'slip covers']:
            cnt['quantity'] += item['quantity']
            cnt['pieces'] += item['quantity'] * variant.pieces
            cnt['cart_total'] += item['quantity'] * item['price']
        cnt[p_group] += item['quantity']

    totals = Counter()

    if state in ('NY', "NJ", "CT", "PA", "DE", "MD", "VA", "WV"):
        gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
        response = gmaps.geocode("%s %s USA" % (state, zipcode))
        if len(response):
            loc = response[0]
            print loc['address_components']
            for obj in loc['address_components']:

                if "administrative_area_level_2" in obj['types']:
                    county = obj['long_name']
                if "locality" in obj['types']:
                    city = obj['long_name']
            if not county:
                county = city
    print (state, county)


    if (state, county) in LOCAL or zipcode in PHILADELPHIA_PLUS:
        if cnt['quantity'] == cnt['ancillary']:
            totals['delivery'] += cnt['ancillary'] * 6999
        else:
            totals['delivery'] += cnt['sectionals'] * 11999
            totals['delivery'] += cnt['upholstery'] * 9999
            totals['delivery'] += cnt['beds'] * 8999
            totals['delivery'] += cnt['dinnete'] * 9999
            totals['delivery'] += cnt['mattress_n_boxspring'] * 7999
            totals['delivery'] += cnt['set_lt_1000'] * 9999
            totals['delivery'] += cnt['set_lt_2000'] * 16999
            totals['delivery'] += cnt['set_gt_2000'] * 19999
            # totals['delivery'] += cnt['chairs'] * 8999

            if cnt['chairs'] == 1:
                totals['delivery'] += cnt['chairs'] * 8999
            elif cnt['chairs'] > 1:
                totals['delivery'] += (cnt['chairs'] * 9999) / 2

            totals['delivery'] += cnt['ancillary'] * 3999
            main_qty = cnt['quantity'] - cnt['ancillary'] - cnt['chairs']
        #     print main_qty
        #     if main_qty:
        #         if main_qty == 1:
        #             totals['delivery'] += 9999
        #         elif cnt['pieces'] <= 15:
        #             totals['delivery'] += 19999
        #         elif cnt['pieces'] > 15:
        #             totals['delivery'] += 27999
        # print totals['delivery']
        tenp = cnt['cart_total'] / 10
        if totals['delivery'] > tenp and tenp > 11999:
            totals['delivery'] = tenp

        totals['delivery'] = 19999 if totals['delivery'] > 19999 else totals['delivery']

        if (state, county) in LOCAL20 or int(zipcode) in PHILADELPHIA_PLUS:
            totals['delivery'] += 2000
        elif (state, county) in LOCAL75 or zipcode in ["11964", "11965"]:
            totals['delivery'] += 7500
        elif (state, county) in LOCAL100:
            totals['delivery'] += 10000

    elif (state, county) in LODESTAR150 + LODESTAR75:
        rate = cnt['cart_total'] * 0.05
        if (state, county) in LODESTAR75:
            totals['delivery'] = 9999 if rate < 9999 else rate
        elif (state, county) in LODESTAR150:
            totals['delivery'] = 14999 if rate < 15000 else rate
        totals['delivery'] += cnt['pieces'] * 500
    else:  # LONG DISTANCE
        for i in range(1, cnt['pieces'] + 1):
            if i == 1:
                totals['delivery'] += 33999
            elif i <= 3:
                totals['delivery'] += 9000
            elif i <= 5:
                totals['delivery'] += 7500
            elif i > 5:
                totals['delivery'] += 6500


    totals['delivery'] += cnt['slipcovers'] * 3000
    return JsonResponse({
       "rates": [
           {
               "service_name": "canadapost-overnight",
               "service_code": "Local",
               "total_price": totals['delivery'],
               "currency": "USD",
           },
       ]
    })
