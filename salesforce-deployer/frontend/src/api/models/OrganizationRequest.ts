/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type OrganizationRequest = {
    name: string;
    instanceUrl: string;
    description?: string;
    type?: OrganizationRequest.type;
    credentials?: {
        username?: string;
        password?: string;
        securityToken?: string;
        clientId?: string;
        clientSecret?: string;
    };
};
export namespace OrganizationRequest {
    export enum type {
        PRODUCTION = 'production',
        SANDBOX = 'sandbox',
        DEVELOPER = 'developer',
        SCRATCH = 'scratch',
    }
}

