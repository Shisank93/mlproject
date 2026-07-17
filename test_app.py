import unittest
from app import app

class FlaskIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        # Configure app for testing
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_landing_page(self):
        """Test that the homepage (index.html) loads successfully with correct branding and stylesheets."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        html = response.data.decode('utf-8')
        # Assert layout brand and references are present
        self.assertIn("EduPredict AI", html)
        self.assertIn("static/css/style.css", html)
        self.assertIn("static/images/hero.png", html)

    def test_predict_form_page(self):
        """Test that the predict form page loads successfully and contains the correct HTML elements."""
        response = self.client.get('/predict')
        self.assertEqual(response.status_code, 200)
        
        html = response.data.decode('utf-8')
        # Assert form tags and parameter names exist
        self.assertIn("<form", html)
        self.assertIn('action="/predict"', html)
        self.assertIn('name="gender"', html)
        self.assertIn('name="ethnicity"', html)
        self.assertIn('name="parental_level_of_education"', html)
        self.assertIn('name="lunch"', html)
        self.assertIn('name="test_preparation_course"', html)
        self.assertIn('name="reading_score"', html)
        self.assertIn('name="writing_score"', html)

    def test_prediction_execution(self):
        """Test that submitting student metrics successfully routes to prediction and displays results."""
        payload = {
            'gender': 'male',
            'ethnicity': 'group C',
            'parental_level_of_education': 'associate\'s degree',
            'lunch': 'standard',
            'test_preparation_course': 'none',
            'reading_score': '75',
            'writing_score': '78'
        }
        response = self.client.post('/predict', data=payload)
        self.assertEqual(response.status_code, 200)
        
        html = response.data.decode('utf-8')
        # Assert the results screen elements exist
        self.assertIn("results-data", html)
        self.assertIn("progressScoreNumber", html)
        self.assertIn("Predict Again", html)
        self.assertIn("Return Home", html)

    def test_about_page(self):
        """Test that the about page loads successfully and contains technical details."""
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn("About the Project", html)
        self.assertIn("Model Objective", html)

    def test_contact_page(self):
        """Test that the contact page loads successfully and contains a contact form."""
        response = self.client.get('/contact')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn("Contact Support", html)
        self.assertIn("Send an Inquiry", html)

if __name__ == "__main__":
    unittest.main()
