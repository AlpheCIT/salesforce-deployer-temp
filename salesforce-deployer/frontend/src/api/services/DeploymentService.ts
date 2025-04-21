/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { DeploymentRequest } from '../models/DeploymentRequest';
import type { DeploymentResponse } from '../models/DeploymentResponse';
import type { DeploymentStatus } from '../models/DeploymentStatus';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class DeploymentService {
    /**
     * Deploy schema to a Salesforce organization
     * Initiates a deployment process to apply schema changes to a target Salesforce organization with configurable validation and rollback options.
     * @param requestBody
     * @returns DeploymentResponse Deployment started
     * @throws ApiError
     */
    public static deploySchema(
        requestBody: DeploymentRequest,
    ): CancelablePromise<DeploymentResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/deployments',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Invalid request`,
                401: `Unauthorized`,
            },
        });
    }
    /**
     * Get deployment status by ID
     * Retrieves the current status, progress, and results of an ongoing or completed deployment operation.
     * @param deploymentId
     * @returns DeploymentStatus Deployment status found
     * @throws ApiError
     */
    public static getDeploymentStatus(
        deploymentId: string,
    ): CancelablePromise<DeploymentStatus> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/deployments/{deploymentId}',
            path: {
                'deploymentId': deploymentId,
            },
            errors: {
                404: `Deployment not found`,
            },
        });
    }
    /**
     * Cancel a deployment
     * Attempts to cancel an in-progress deployment operation, rolling back any changes if possible based on the deployment phase.
     * @param deploymentId
     * @returns DeploymentStatus Deployment cancelled successfully
     * @throws ApiError
     */
    public static cancelDeployment(
        deploymentId: string,
    ): CancelablePromise<DeploymentStatus> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/deployments/{deploymentId}/cancel',
            path: {
                'deploymentId': deploymentId,
            },
            errors: {
                400: `Deployment cannot be cancelled`,
                404: `Deployment not found`,
            },
        });
    }
}
