/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { DashboardMetadata } from './DashboardMetadata';
import type { FlowMetadata } from './FlowMetadata';
import type { ObjectMetadata } from './ObjectMetadata';
import type { WorkflowMetadata } from './WorkflowMetadata';
export type Schema = {
    /**
     * Schema ID
     */
    id: string;
    /**
     * Schema name
     */
    name: string;
    /**
     * Schema description
     */
    description?: string;
    /**
     * Schema creation timestamp
     */
    createdAt?: string;
    /**
     * Schema last update timestamp
     */
    updatedAt?: string;
    /**
     * ID of the source organization
     */
    sourceOrgId?: string;
    /**
     * Salesforce API version
     */
    apiVersion?: string;
    components?: {
        objects?: Record<string, ObjectMetadata>;
        workflowRules?: Record<string, WorkflowMetadata>;
        dashboards?: Record<string, DashboardMetadata>;
        flows?: Record<string, FlowMetadata>;
    };
};

