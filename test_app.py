import unittest
import json
from app import app

class RailwayApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_male_senior_discount(self):
        # Male age 65 -> 30% discount -> Rs. 700
        res = self.app.post('/api/calculate', json={'gender': 'male', 'age': 65})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['category'], 'Senior Citizen')
        self.assertEqual(data['discount_percent'], 30)
        self.assertEqual(data['final_price'], 700)

    def test_male_normal(self):
        # Male age 45 -> 0% discount -> Rs. 1000
        res = self.app.post('/api/calculate', json={'gender': 'male', 'age': 45})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['category'], 'Normal Citizen')
        self.assertEqual(data['discount_percent'], 0)
        self.assertEqual(data['final_price'], 1000)

    def test_female_senior_discount(self):
        # Female age 60 -> 50% discount -> Rs. 500
        res = self.app.post('/api/calculate', json={'gender': 'female', 'age': 60})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['category'], 'Senior Citizen')
        self.assertEqual(data['discount_percent'], 50)
        self.assertEqual(data['final_price'], 500)

    def test_female_normal_discount(self):
        # Female age 30 -> 30% discount -> Rs. 700
        res = self.app.post('/api/calculate', json={'gender': 'female', 'age': 30})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['category'], 'Normal Citizen')
        self.assertEqual(data['discount_percent'], 30)
        self.assertEqual(data['final_price'], 700)

    def test_invalid_age_negative(self):
        res = self.app.post('/api/calculate', json={'gender': 'male', 'age': -5})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Please enter the valid age')

    def test_invalid_age_over_200(self):
        res = self.app.post('/api/calculate', json={'gender': 'female', 'age': 205})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 'Please enter the valid age')

if __name__ == '__main__':
    unittest.main()
