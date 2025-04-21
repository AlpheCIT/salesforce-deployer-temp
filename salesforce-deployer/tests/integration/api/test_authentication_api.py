# coding: utf-8

from fastapi.testclient import TestClient


from src.models.authentication_response import AuthenticationResponse  # noqa: F401
from src.models.error_response import ErrorResponse  # noqa: F401
from src.models.login_request import LoginRequest  # noqa: F401
from src.models.o_auth_request import OAuthRequest  # noqa: F401


def test_authenticate_with_credentials(client: TestClient):
    """Test case for authenticate_with_credentials

    Authenticate with Salesforce credentials
    """
    login_request = {"security_token":"ABCDEFGHIJKLMNOP","password":"myPassword123","username":"user@example.com","instance_url":"https://login.salesforce.com"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/auth/login",
    #    headers=headers,
    #    json=login_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_authenticate_with_o_auth(client: TestClient):
    """Test case for authenticate_with_o_auth

    Authenticate using OAuth 2.0
    """
    o_auth_request = {"redirect_uri":"https://localhost:8000/callback","password":"myPassword123","client_id":"3MVG9e2mBbZnmcolVXiRm8YNot7VI5W_oiqJuBDdDUNF9s45MfoiV2h_nI2paMT1QA_yw3UxQncI7Goz8L1A7","auth_code":"aPrxJZTWTs65VeNEEhYht92nXyz","client_secret":"123456789012345678","username":"user@example.com"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/auth/oauth",
    #    headers=headers,
    #    json=o_auth_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_refresh_token(client: TestClient):
    """Test case for refresh_token

    Refresh authentication token
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/auth/refresh",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

