/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Organization } from '../models/Organization';
import type { OrganizationRequest } from '../models/OrganizationRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class OrganizationsService {
    /**
     * Get a list of connected Salesforce organizations
     * Retrieves all Salesforce organizations that have been configured for schema extraction and deployment operations.
     * @returns Organization List of organizations retrieved successfully
     * @throws ApiError
     */
    public static getOrganizations(): CancelablePromise<Array<Organization>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/organizations',
            errors: {
                401: `Unauthorized`,
            },
        });
    }
    /**
     * Add a new Salesforce organization
     * Registers a new Salesforce organization with the system, including connection credentials and organization metadata.
     * @param requestBody
     * @returns Organization Organization added successfully
     * @throws ApiError
     */
    public static addOrganization(
        requestBody: OrganizationRequest,
    ): CancelablePromise<Organization> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/organizations',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Invalid request`,
            },
        });
    }
    /**
     * Get organization details by ID
     * Retrieves detailed information about a specific Salesforce organization, including its connection status and metadata.
     * @param orgId
     * @returns Organization Organization details retrieved successfully
     * @throws ApiError
     */
    public static getOrganizationById(
        orgId: string,
    ): CancelablePromise<Organization> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/organizations/{orgId}',
            path: {
                'orgId': orgId,
            },
            errors: {
                404: `Organization not found`,
            },
        });
    }
    /**
     * Update organization details
     * Updates the configuration, credentials, or metadata for an existing Salesforce organization connection.
     * @param orgId
     * @param requestBody
     * @returns Organization Organization updated successfully
     * @throws ApiError
     */
    public static updateOrganization(
        orgId: string,
        requestBody: OrganizationRequest,
    ): CancelablePromise<Organization> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/organizations/{orgId}',
            path: {
                'orgId': orgId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Invalid request`,
                404: `Organization not found`,
            },
        });
    }
    /**
     * Delete organization
     * Removes a Salesforce organization from the system, including all stored credentials and connection information.
     * @param orgId
     * @returns void
     * @throws ApiError
     */
    public static deleteOrganization(
        orgId: string,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/organizations/{orgId}',
            path: {
                'orgId': orgId,
            },
            errors: {
                404: `Organization not found`,
            },
        });
    }
}
