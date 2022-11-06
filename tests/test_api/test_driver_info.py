import unittest

from app import create_app
from database.create_test_database import create_db


class TestDriversApi(unittest.TestCase):
    """Test Driver info api"""
    def setUp(self):
        """Test constructor"""
        app = create_app('testing')
        self.db = app.config['db']
        create_db(db=self.db)
        self.ctx = app.test_request_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        """Test destructor"""
        self.ctx.pop()

    def test_default_format(self):
        """Test with default value format=json"""
        response = self.client.get('/api/v1/drivers/BHS/')
        data = response.json
        code = response.status_code
        self.assertEqual(code, 200)
        self.assertEqual({'abbr': 'BHS', 'name': 'Brendon Hartley'}, data)

    def test_xml_format(self):
        """Test with value format=xml"""
        response = self.client.get('/api/v1/drivers/BHS/?format=xml')
        data = response.get_data(as_text=True)
        code = response.status_code
        self.assertEqual(code, 200)
        self.assertIn('Brendon Hartley', data)

    def test_wrong_driver(self):
        """Test with default value format=json"""
        response = self.client.get('/api/v1/drivers/BHL/')
        data = response.json
        code = response.status_code
        self.assertEqual(code, 404)
        self.assertEqual({'error': 'driver not found'}, data)


if __name__ == "__main__":
    unittest.main()
