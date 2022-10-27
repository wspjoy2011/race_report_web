import unittest
from app import create_app
import xml.etree.ElementTree as ET

app = create_app()


class TestDriversApi(unittest.TestCase):
    """Test Race report api"""
    def setUp(self):
        """Test constructor"""
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        """Test destructor"""
        self.ctx.pop()

    def test_default_values(self):
        """Test with default values(order=asc, format=json)"""
        with app.app_context(), app.test_request_context():
            response = self.client.get('/api/v1/report/')
            data = response.json
            code = response.status_code
            self.assertEqual(code, 200)
            self.assertEqual({
                'company': 'FERRARI',
                'driver': 'Sebastian Vettel',
                'place': 1,
                'time': '0:01:04.415000'}, data.pop(0))

    def test_order_desc(self):
        """Test with order=desc, format=json"""
        with app.app_context(), app.test_request_context():
            response = self.client.get('/api/v1/report/?order=desc')
            data = response.json
            code = response.status_code
            self.assertEqual(code, 200)
            self.assertEqual({
                'company': 'MERCEDES',
                'driver': 'Lewis Hamilton',
                'place': 1,
                'time': '0:06:47.540000'}, data.pop(0))

    def test_xml_default_order(self):
        """Test with order=asc, format=xml"""
        with app.app_context(), app.test_request_context():
            response = self.client.get('/api/v1/report/?format=xml')
            data = response.get_data(as_text=True)
            root = ET.ElementTree(ET.fromstring(data))
            first_driver = str(ET.tostring(root.find("Race")))
            code = response.status_code
            self.assertEqual(code, 200)
            self.assertIn('Sebastian Vettel', first_driver)

    def test_xml_desc_order(self):
        """Test with order=desc, format=xml"""
        with app.app_context(), app.test_request_context():
            response = self.client.get('/api/v1/report/?order=desc&format=xml')
            data = response.get_data(as_text=True)
            root = ET.ElementTree(ET.fromstring(data))
            last_driver = str(ET.tostring(root.find("Race")))
            code = response.status_code
            self.assertEqual(code, 200)
            self.assertIn('Lewis Hamilton', last_driver)

    def test_wrong_order(self):
        """Test with default values(order=wrong, format=wrong)"""
        with app.app_context(), app.test_request_context():
            response = self.client.get('/api/v1/report/?order=wrong')
            data = response.json
            code = response.status_code
            self.assertEqual(code, 404)
            self.assertIn('The requested URL was not found on the server', data['message'])
