/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type SchemaComparisonRequest = {
    /**
     * ID of the source schema
     */
    sourceSchemaId: string;
    /**
     * ID of the target schema
     */
    targetSchemaId: string;
    /**
     * List of components to compare. If not provided, all components will be compared.
     */
    components?: Array<'objects' | 'fields' | 'workflows' | 'dashboards' | 'flows'>;
};

