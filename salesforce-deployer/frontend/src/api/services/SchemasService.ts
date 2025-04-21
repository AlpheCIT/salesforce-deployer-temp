/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Schema } from '../models/Schema';
import type { SchemaComparisonRequest } from '../models/SchemaComparisonRequest';
import type { SchemaComparisonResponse } from '../models/SchemaComparisonResponse';
import type { SchemaExtractionRequest } from '../models/SchemaExtractionRequest';
import type { SchemaExtractionResponse } from '../models/SchemaExtractionResponse';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class SchemasService {
    /**
     * Extract schema from a Salesforce organization
     * Extracts metadata schema components from a specified Salesforce organization, with options to filter by component types and include standard or managed components.
     * @param requestBody
     * @returns SchemaExtractionResponse Schema extraction successful
     * @throws ApiError
     */
    public static extractSchema(
        requestBody: SchemaExtractionRequest,
    ): CancelablePromise<SchemaExtractionResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/schemas/extract',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Invalid request`,
                401: `Unauthorized`,
            },
        });
    }
    /**
     * Get schema by ID
     * Retrieves the complete metadata schema definition by its unique identifier, including all component definitions and relationships.
     * @param schemaId
     * @returns Schema Schema found
     * @throws ApiError
     */
    public static getSchema(
        schemaId: string,
    ): CancelablePromise<Schema> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/schemas/{schemaId}',
            path: {
                'schemaId': schemaId,
            },
            errors: {
                404: `Schema not found`,
            },
        });
    }
    /**
     * Update schema by ID
     * Updates an existing schema definition with new metadata components, properties, or relationships while preserving its identifier.
     * @param schemaId
     * @param requestBody
     * @returns Schema Schema updated successfully
     * @throws ApiError
     */
    public static updateSchema(
        schemaId: string,
        requestBody: Schema,
    ): CancelablePromise<Schema> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/schemas/{schemaId}',
            path: {
                'schemaId': schemaId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Invalid request`,
                404: `Schema not found`,
            },
        });
    }
    /**
     * Delete schema by ID
     * Permanently removes a schema definition and all its associated metadata components from the system.
     * @param schemaId
     * @returns void
     * @throws ApiError
     */
    public static deleteSchema(
        schemaId: string,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/schemas/{schemaId}',
            path: {
                'schemaId': schemaId,
            },
            errors: {
                404: `Schema not found`,
            },
        });
    }
    /**
     * Compare two schemas
     * Performs a detailed comparison between two schemas, identifying added, modified, and removed components with field-level change tracking.
     * @param requestBody
     * @returns SchemaComparisonResponse Schema comparison completed
     * @throws ApiError
     */
    public static compareSchemas(
        requestBody: SchemaComparisonRequest,
    ): CancelablePromise<SchemaComparisonResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/schemas/compare',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Invalid request`,
            },
        });
    }
}
