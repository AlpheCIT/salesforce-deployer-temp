/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type WorkflowMetadata = {
    name?: string;
    object?: string;
    active?: boolean;
    description?: string;
    criteria?: string;
    actions?: Array<{
        type?: 'FieldUpdate' | 'EmailAlert' | 'OutboundMessage' | 'Task';
        name?: string;
        field?: string;
        value?: string;
    }>;
};

