/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type SchemaExtractionRequest = {
    /**
     * ID of the organization to extract schema from
     */
    orgId: string;
    /**
     * List of components to extract. If not provided, all components will be extracted.
     */
    components?: Array<'objects' | 'fields' | 'workflows' | 'dashboards' | 'flows'>;
    /**
     * Whether to include standard objects
     */
    includeStandard?: boolean;
    /**
     * Whether to include managed package components
     */
    includeManaged?: boolean;
    /**
     * Filter expression to limit extracted components
     */
    filter?: string;
};

