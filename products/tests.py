from django.test import TestCase, Client

# Create your tests here.
class ProductTestCase(TestCase):

    def test_product_list_view(self):
        c = Client()
        response = c.get('/products')
        self.assertEqual(response.status_code, 200)
