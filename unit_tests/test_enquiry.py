import unittest
from unittest.mock import patch
from enquiry_api import app
from flask import json


class EnquiryApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.ctx = self.app.app_context()
        self.ctx.push()

    @patch('enquiry_api.sql.Sql.get_all_enquirys')
    def test_get_enquirys(self, mock_get_all_enquirys):
        # Mocking the Sql.get_all_enquirys method
        mock_get_all_enquirys.return_value = [{'id': '1', 'name': 'Test Enquiry'}]

        # Make a test call to the API
        response = self.client.get('/get_enquirys/1')
        data = json.loads(response.get_data(as_text=True))

        # Assert status code and response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Test Enquiry')

    @patch('enquiry_api.sql.Sql.new_enquiry')
    def test_new_enquiry(self, mock_new_enquiry):
        # Mocking the Sql.new_enquiry method
        mock_new_enquiry.return_value = {'id': '1', 'name': 'New Enquiry'}

        # Data to be sent with POST request
        data = {'name': 'New Enquiry', 'other_data': '123'}
        response = self.client.post('/new_enquiry', json=data)

        # Assert status code and response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response_data[0]['name'], 'New Enquiry')

if __name__ == '__main__':
    unittest.main()
