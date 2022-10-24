import unittest
from app import app

from flask import url_for


class AppTestCase(unittest.TestCase):
    """Test app"""
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_index_page(self):
        """Test index page"""
        with app.app_context(), app.test_request_context():
            response = self.client.get(url_for('index'))
            data = response.get_data(as_text=True)
            code = response.status_code
            self.assertEqual(code, 200)
            self.assertIn('F1 Monaco Race 2018', data)

    def test_top_driver(self):
        """Test correct top driver in left panel"""
        with app.app_context(), app.test_request_context():
            response = self.client.get(url_for('index'))
            data = response.get_data(as_text=True)
            code = response.status_code
            self.assertEqual(code, 200)
            self.assertIn('1. Sebastian Vettel', data)

    def test_report_default(self):
        """Test report by default"""
        with app.app_context(), app.test_request_context():
            response = self.client.get(url_for('show_report'))
            data = response.get_data(as_text=True)
            code = response.status_code
            answer = '<td>1</td>\n        <td>Sebastian Vettel</td>\n' \
                     '        <td>FERRARI</td>\n        <td>0:01:04.415000</td>\n'
            self.assertEqual(code, 200)
            self.assertIn(answer, data)

    def test_report_order_asc(self):
        """Test report by asc order"""
        with app.app_context(), app.test_request_context():
            response = self.client.get(url_for('show_report', order='asc'))
            data = response.get_data(as_text=True)
            code = response.status_code
            answer = '<td>1</td>\n        <td>Sebastian Vettel</td>\n' \
                     '        <td>FERRARI</td>\n        <td>0:01:04.415000</td>\n'
            self.assertEqual(code, 200)
            self.assertIn(answer, data)

    def test_report_order_desc(self):
        """Test report by desc order"""
        with app.app_context(), app.test_request_context():
            response = self.client.get(url_for('show_report', order='desc'))
            data = response.get_data(as_text=True)
            code = response.status_code
            answer = '<td>1</td>\n        <td>Lewis Hamilton</td>\n' \
                     '        <td>MERCEDES</td>\n        <td>0:06:47.540000</td>\n'
            self.assertEqual(code, 200)
            self.assertIn(answer, data)

    def test_drivers(self):
        """Test drivers"""
        with app.app_context(), app.test_request_context():
            response = self.client.get(url_for('show_drivers'))
            data = response.get_data(as_text=True)
            code = response.status_code
            answer = '<a href="/report/drivers/?driver_id=BHS">BHS</a>'
            self.assertEqual(code, 200)
            self.assertIn(answer, data)

    def test_driver_profile(self):
        """Test driver profile page"""
        with app.app_context(), app.test_request_context():
            response = self.client.get(url_for('show_drivers', driver_id='BHS'))
            data = response.get_data(as_text=True)
            code = response.status_code
            answer = 'BHS'
            self.assertEqual(code, 200)
            self.assertIn(answer, data)

    def test_driver_profile_wrong(self):
        """Test driver profile wrong page"""
        with app.app_context(), app.test_request_context():
            response = self.client.get(url_for('show_drivers', driver_id='wrong'))
            data = response.get_data(as_text=True)
            code = response.status_code
            answer = 'Not Found'
            self.assertEqual(code, 200)
            self.assertIn(answer, data)

    def test_report_order_wrong(self):
        """Test report by wrong order"""
        with app.app_context(), app.test_request_context():
            response = self.client.get(url_for("show_report", order='wrong'))
            data = response.get_data(as_text=True)
            code = response.status_code
            answer = '404 Not Found'
            self.assertEqual(code, 404)
            self.assertIn(answer, data)

    def test_wrong_urls(self):
        """Test wrong url"""
        with app.app_context(), app.test_request_context():
            response = self.client.get("/wrong/")
            data = response.get_data(as_text=True)
            code = response.status_code
            answer = '404 Not Found'
            self.assertEqual(code, 404)
            self.assertIn(answer, data)


if __name__ == "__main__":
    unittest.main()
