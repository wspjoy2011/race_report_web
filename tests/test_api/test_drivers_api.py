import unittest
import xml.etree.ElementTree as ET

from app import create_app
from database.create_test_database import create_db


class TestDriversApi(unittest.TestCase):
    """Test Drivers api"""
    def setUp(self):
        """Test constructor"""
        app = create_app('testing')
        self.db = app.config['db']
        create_db(db=self.db)
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        """Test destructor"""
        self.ctx.pop()

    def test_default_values(self):
        """Test with default values(order=asc, format=json)"""
        response = self.client.get('/api/v1/drivers/')
        data = response.json
        code = response.status_code
        self.assertEqual(code, 200)
        self.assertEqual({'abbr': 'BHS', 'name': 'Brendon Hartley'}, data.pop(0))

    def test_order_desc(self):
        """Test with order=desc, format=json"""
        response = self.client.get('/api/v1/drivers/?order=desc')
        data = response.json
        code = response.status_code
        self.assertEqual(code, 200)
        self.assertEqual({'abbr': 'BHS', 'name': 'Brendon Hartley'}, data.pop())

    def test_xml_default_order(self):
        """Test with order=asc, format=xml"""
        response = self.client.get('/api/v1/drivers/?format=xml')
        data = response.get_data(as_text=True)
        root = ET.ElementTree(ET.fromstring(data))
        first_driver = str(ET.tostring(root.find("Driver")))
        code = response.status_code
        self.assertEqual(code, 200)
        self.assertIn('Brendon Hartley', first_driver)

    def test_xml_desc_order(self):
        """Test with order=desc, format=xml"""
        response = self.client.get('/api/v1/drivers/?order=desc&format=xml')
        data = response.get_data(as_text=True)
        root = ET.ElementTree(ET.fromstring(data))
        last_driver = str(ET.tostring(root.find("Driver")))
        code = response.status_code
        self.assertEqual(code, 200)
        self.assertIn('Valtteri Bottas', last_driver)

    def test_wrong_order(self):
        """Test with default values(order=wrong, format=wrong)"""
        response = self.client.get('/api/v1/drivers/?order=wrong')
        data = response.json
        code = response.status_code
        self.assertEqual(code, 404)
        self.assertIn('The requested URL was not found on the server', data['message'])


if __name__ == "__main__":
    unittest.main()
