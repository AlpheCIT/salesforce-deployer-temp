/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type FlowMetadata = {
    name?: string;
    label?: string;
    description?: string;
    status?: FlowMetadata.status;
    processType?: FlowMetadata.processType;
    triggerType?: string;
    eventType?: string;
};
export namespace FlowMetadata {
    export enum status {
        ACTIVE = 'Active',
        DRAFT = 'Draft',
        OBSOLETE = 'Obsolete',
    }
    export enum processType {
        FLOW = 'Flow',
        AUTO_LAUNCHED_FLOW = 'AutoLaunchedFlow',
        WORKFLOW = 'Workflow',
    }
}

