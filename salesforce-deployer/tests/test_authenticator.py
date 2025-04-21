from unittest import TestCase
from src.core.authenticator import SalesforceAuthenticator

class TestSalesforceAuthenticator(TestCase):
    def setUp(self):
        self.authenticator = SalesforceAuthenticator()

    def test_authenticate_success(self):
        # Mock successful authentication
        self.authenticator.username = "test_user"
        self.authenticator.password = "test_password"
        self.authenticator.security_token = "test_token"
        
        result = self.authenticator.authenticate()
        self.assertTrue(result)

    def test_authenticate_failure(self):
        """Test authentication failure with Salesforce."""
        # Create authenticator with bad credentials to trigger failure
        authenticator = SalesforceAuthenticator(username="bad_user", password="bad_pass")
        
        # Force instance_url to None for this test
        authenticator.instance_url = None
        
        # This should raise ValueError
        with self.assertRaises(ValueError):
            authenticator.authenticate()

    def test_missing_credentials(self):
        # Test missing credentials
        self.authenticator.username = None
        self.authenticator.password = None
        
        with self.assertRaises(ValueError):
            self.authenticator.authenticate()