import unittest
from app import create_app

from flask import url_for

app = create_app()


class AppTestCase(unittest.TestCase):
    """Test app"""
    def setUp(self):
        self.ctx = app.test_request_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_index_page(self):
        """Test index page"""
        response = self.client.get(url_for('main.index'))
        data = response.get_data(as_text=True)
        code = response.status_code
        self.assertEqual(code, 200)
        self.assertIn('F1 Monaco Race 2018', data)

    def test_top_driver(self):
        """Test correct top driver in left panel"""
        response = self.client.get(url_for('main.index'))
        data = response.get_data(as_text=True)
        code = response.status_code
        self.assertEqual(code, 200)
        self.assertIn('1. Sebastian Vettel', data)

    def test_report_default(self):
        """Test report by default"""
        response = self.client.get(url_for('main.show_report'))
        data = response.get_data(as_text=True)
        code = response.status_code
        answer = '<td>1</td>\n        <td>Sebastian Vettel</td>\n' \
                 '        <td>FERRARI</td>\n        <td>0:01:04.415000</td>\n'
        self.assertEqual(code, 200)
        self.assertIn(answer, data)

    def test_report_order_asc(self):
        """Test report by asc order"""
        response = self.client.get(url_for('main.show_report', order='asc'))
        data = response.get_data(as_text=True)
        code = response.status_code
        answer = '<td>1</td>\n        <td>Sebastian Vettel</td>\n' \
                 '        <td>FERRARI</td>\n        <td>0:01:04.415000</td>\n'
        self.assertEqual(code, 200)
        self.assertIn(answer, data)

    def test_report_order_desc(self):
        """Test report by desc order"""
        response = self.client.get(url_for('main.show_report', order='desc'))
        data = response.get_data(as_text=True)
        code = response.status_code
        answer = '<td>1</td>\n        <td>Lewis Hamilton</td>\n' \
                 '        <td>MERCEDES</td>\n        <td>0:06:47.540000</td>\n'
        self.assertEqual(code, 200)
        self.assertIn(answer, data)

    def test_drivers(self):
        """Test drivers"""
        response = self.client.get(url_for('main.show_drivers'))
        data = response.get_data(as_text=True)
        code = response.status_code
        answer = '<a href="/report/drivers/?driver_id=BHS">BHS</a>'
        self.assertEqual(code, 200)
        self.assertIn(answer, data)

    def test_driver_profile(self):
        """Test driver profile page"""
        response = self.client.get(url_for('main.show_drivers', driver_id='BHS'))
        data = response.get_data(as_text=True)
        code = response.status_code
        answer = 'BHS'
        self.assertEqual(code, 200)
        self.assertIn(answer, data)

    def test_driver_profile_wrong(self):
        """Test driver profile wrong page"""
        response = self.client.get(url_for('main.show_drivers', driver_id='wrong'))
        data = response.get_data(as_text=True)
        code = response.status_code
        answer = 'Not Found'
        self.assertEqual(code, 200)
        self.assertIn(answer, data)

    def test_report_order_wrong(self):
        """Test report by wrong order"""
        response = self.client.get(url_for("main.show_report", order='wrong'))
        data = response.get_data(as_text=True)
        code = response.status_code
        answer = '404 Not Found'
        self.assertEqual(code, 404)
        self.assertIn(answer, data)

    def test_wrong_urls(self):
        """Test wrong url"""
        response = self.client.get("/wrong/")
        data = response.get_data(as_text=True)
        code = response.status_code
        answer = '404 Not Found'
        self.assertEqual(code, 404)
        self.assertIn(answer, data)


if __name__ == "__main__":
    unittest.main()
