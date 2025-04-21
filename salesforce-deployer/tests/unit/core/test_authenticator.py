import unittest
from unittest.mock import patch, MagicMock
import os
import tempfile

from src.core.authenticator import SalesforceAuthenticator


class TestAuthenticator(unittest.TestCase):

    def setUp(self):
        """Set up test environment."""
        # Create temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        
        # Create test .env file
        self.env_file = os.path.join(self.test_dir, ".env")
        with open(self.env_file, 'w') as f:
            f.write("SF_USERNAME=test@example.com\n")
            f.write("SF_PASSWORD=password123\n")
            f.write("SF_SECURITY_TOKEN=token123\n")
            f.write("SF_INSTANCE_URL=https://test.salesforce.com\n")
        
        # Default authenticator for tests
        self.authenticator = SalesforceAuthenticator(
            username="test_user",
            password="test_password",
            security_token="test_token"
        )

    @patch.dict('os.environ', {
        'SF_USERNAME': 'test@example.com',
        'SF_PASSWORD': 'password123',
        'SF_SECURITY_TOKEN': 'token123',
        'SF_INSTANCE_URL': 'https://test.salesforce.com'
    })
    @patch('requests.post')
    def test_authenticate_success(self, mock_post):
        """Test successful authentication with Salesforce."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'test_token',
            'instance_url': 'https://test.salesforce.com'
        }
        mock_post.return_value = mock_response
        
        # Create authenticator and authenticate
        authenticator = SalesforceAuthenticator()
        result = authenticator.authenticate()
        
        # Verify authentication
        self.assertTrue(result)
        self.assertEqual(authenticator.access_token, 'test_token')
        self.assertEqual(authenticator.instance_url, 'https://test.salesforce.com')
        mock_post.assert_called_once()
        
    @patch.dict('os.environ', {
        'SF_USERNAME': 'test@example.com',
        'SF_PASSWORD': 'password123',
        'SF_SECURITY_TOKEN': 'token123',
        'SF_INSTANCE_URL': 'https://test.salesforce.com'
    })
    @patch('requests.post')
    def test_authenticate_failure(self, mock_post):
        """Test failed authentication with Salesforce."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            'error': 'invalid_grant',
            'error_description': 'authentication failure'
        }
        mock_post.return_value = mock_response
        
        # Create authenticator and authenticate
        authenticator = SalesforceAuthenticator()
        result = authenticator.authenticate()
        
        # Verify authentication failure
        self.assertFalse(result)
        self.assertIsNone(authenticator.access_token)
        self.assertIsNone(authenticator.instance_url)

    def test_authenticate_failure(self):
        """Test authentication failure."""
        # Create authenticator with known bad credentials
        authenticator = SalesforceAuthenticator(username="bad_user", password="bad_pass")
        
        # Explicitly set instance_url to None for this test
        authenticator.instance_url = None
        
        # Test that ValueError is raised
        with self.assertRaises(ValueError):
            authenticator.authenticate()
        
        # Instance URL should still be None after failed auth
        self.assertIsNone(authenticator.instance_url)


if __name__ == "__main__":
    unittest.main()