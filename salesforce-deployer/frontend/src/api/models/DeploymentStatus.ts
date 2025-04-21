/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ApexTestResult } from './ApexTestResult';
import type { ComponentResult } from './ComponentResult';
export type DeploymentStatus = {
    /**
     * Deployment ID
     */
    deploymentId: string;
    /**
     * Deployment status
     */
    status: DeploymentStatus.status;
    /**
     * Progress percentage
     */
    progress?: number;
    /**
     * Deployment start time
     */
    startTime?: string;
    /**
     * Deployment end time
     */
    endTime?: string;
    /**
     * Additional information
     */
    message?: string;
    results?: {
        /**
         * Whether the deployment was successful
         */
        success?: boolean;
        /**
         * Completion timestamp
         */
        completedDate?: string;
        componentFailures?: Array<ComponentResult>;
        componentSuccesses?: Array<ComponentResult>;
        componentErrors?: Array<ComponentResult>;
        apexTestResults?: Array<ApexTestResult>;
    };
};
export namespace DeploymentStatus {
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

