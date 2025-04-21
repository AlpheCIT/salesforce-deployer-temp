/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { SchemaValidationResponse } from './SchemaValidationResponse';
export type DeploymentResponse = {
    /**
     * Deployment ID
     */
    deploymentId: string;
    /**
     * Deployment status
     */
    status: DeploymentResponse.status;
    /**
     * Additional information
     */
    message?: string;
    validationResults?: SchemaValidationResponse;
};
export namespace DeploymentResponse {
    /**
     * Deployment status
     */
    export enum status {
        QUEUED = 'queued',
        IN_PROGRESS = 'in_progress',
        COMPLETED = 'completed',
        FAILED = 'failed',
        CANCELLED = 'cancelled',
    }
}

