/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type AuthenticationResponse = {
    /**
     * JWT access token
     */
    accessToken: string;
    /**
     * JWT refresh token
     */
    refreshToken?: string;
    /**
     * Salesforce instance URL
     */
    instanceUrl: string;
    /**
     * Token expiration time in seconds
     */
    expiresIn?: number;
};

