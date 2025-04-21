/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type ErrorResponse = {
    /**
     * Error code
     */
    error: string;
    /**
     * Error message
     */
    message: string;
    /**
     * Detailed error information
     */
    details?: Array<{
        field?: string;
        message?: string;
    }>;
};

