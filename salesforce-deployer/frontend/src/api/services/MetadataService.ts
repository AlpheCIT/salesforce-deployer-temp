/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { FieldMetadata } from '../models/FieldMetadata';
import type { ObjectMetadata } from '../models/ObjectMetadata';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class MetadataService {
    /**
     * Get a list of objects
     * Retrieves a list of all available objects from either a stored schema or directly from a connected Salesforce organization.
     * @param schemaId ID of the schema to get objects from. If not provided, objects from the connected Salesforce org will be returned.
     * @returns ObjectMetadata List of objects retrieved successfully
     * @throws ApiError
     */
    public static getObjects(
        schemaId?: string,
    ): CancelablePromise<Array<ObjectMetadata>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/metadata/objects',
            query: {
                'schemaId': schemaId,
            },
            errors: {
                401: `Unauthorized`,
            },
        });
    }
    /**
     * Get object details by name
     * Fetches comprehensive metadata for a specific object, including its fields, relationships, and configuration properties.
     * @param objectName
     * @param schemaId ID of the schema to get the object from. If not provided, the object from the connected Salesforce org will be returned.
     * @returns ObjectMetadata Object details retrieved successfully
     * @throws ApiError
     */
    public static getObjectByName(
        objectName: string,
        schemaId?: string,
    ): CancelablePromise<ObjectMetadata> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/metadata/objects/{objectName}',
            path: {
                'objectName': objectName,
            },
            query: {
                'schemaId': schemaId,
            },
            errors: {
                404: `Object not found`,
            },
        });
    }
    /**
     * Get fields for an object
     * Returns a list of all fields defined for a specific object, with their data types, validation rules, and relationships.
     * @param objectName
     * @param schemaId ID of the schema to get fields from. If not provided, fields from the connected Salesforce org will be returned.
     * @returns FieldMetadata Fields retrieved successfully
     * @throws ApiError
     */
    public static getObjectFields(
        objectName: string,
        schemaId?: string,
    ): CancelablePromise<Array<FieldMetadata>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/metadata/objects/{objectName}/fields',
            path: {
                'objectName': objectName,
            },
            query: {
                'schemaId': schemaId,
            },
            errors: {
                404: `Object not found`,
            },
        });
    }
}
