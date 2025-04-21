/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AuthenticationResponse } from '../models/AuthenticationResponse';
import type { LoginRequest } from '../models/LoginRequest';
import type { OAuthRequest } from '../models/OAuthRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class AuthenticationService {
    /**
     * Authenticate with Salesforce credentials
     * Authenticates a user with their Salesforce username, password, and optional security token to obtain an access token for API access.
     * @param requestBody
     * @returns AuthenticationResponse Authentication successful
     * @throws ApiError
     */
    public static authenticateWithCredentials(
        requestBody: LoginRequest,
    ): CancelablePromise<AuthenticationResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/auth/login',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                401: `Authentication failed`,
            },
        });
    }
    /**
     * Authenticate using OAuth 2.0
     * Authenticates using the OAuth 2.0 protocol, supporting both web server flow (with auth code) and username-password flow for headless integrations.
     * @param requestBody
     * @returns AuthenticationResponse Authentication successful
     * @throws ApiError
     */
    public static authenticateWithOAuth(
        requestBody: OAuthRequest,
    ): CancelablePromise<AuthenticationResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/auth/oauth',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                401: `Authentication failed`,
            },
        });
    }
    /**
     * Refresh authentication token
     * Obtains a new access token using a valid refresh token when the current token has expired or is about to expire.
     * @returns AuthenticationResponse Token refreshed successfully
     * @throws ApiError
     */
    public static refreshToken(): CancelablePromise<AuthenticationResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/auth/refresh',
            errors: {
                401: `Invalid or expired refresh token`,
            },
        });
    }
}
