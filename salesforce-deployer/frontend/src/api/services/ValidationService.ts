/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { SchemaValidationRequest } from '../models/SchemaValidationRequest';
import type { SchemaValidationResponse } from '../models/SchemaValidationResponse';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ValidationService {
    /**
     * Validate a schema
     * Analyzes a schema for validity, checking component dependencies, references, and compatibility with target Salesforce organizations.
     * @param requestBody
     * @returns SchemaValidationResponse Schema validation completed
     * @throws ApiError
     */
    public static validateSchema(
        requestBody: SchemaValidationRequest,
    ): CancelablePromise<SchemaValidationResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/schemas/validate',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Invalid request`,
            },
        });
    }
}
