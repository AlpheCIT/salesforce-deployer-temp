/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type Organization = {
    id?: string;
    name?: string;
    instanceUrl?: string;
    description?: string;
    type?: Organization.type;
    createdAt?: string;
    lastConnected?: string;
};
export namespace Organization {
    export enum type {
        PRODUCTION = 'production',
        SANDBOX = 'sandbox',
        DEVELOPER = 'developer',
        SCRATCH = 'scratch',
    }
}

