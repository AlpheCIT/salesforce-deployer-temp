/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type OAuthRequest = {
    /**
     * OAuth client ID
     */
    clientId: string;
    /**
     * OAuth client secret
     */
    clientSecret: string;
    /**
     * OAuth redirect URI
     */
    redirectUri?: string;
    /**
     * OAuth authorization code (required if not using username/password flow)
     */
    authCode?: string;
    /**
     * Salesforce username (required if using username/password flow)
     */
    username?: string;
    /**
     * Salesforce password (required if using username/password flow)
     */
    password?: string;
};

