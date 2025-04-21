/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type SchemaExtractionResponse = {
    /**
     * ID of the extracted schema
     */
    schemaId: string;
    /**
     * Status of the extraction process
     */
    status: SchemaExtractionResponse.status;
    /**
     * Progress percentage
     */
    progress?: number;
    /**
     * Additional information
     */
    message?: string;
    stats?: {
        /**
         * Number of objects extracted
         */
        objects?: number;
        /**
         * Number of fields extracted
         */
        fields?: number;
        /**
         * Number of workflow rules extracted
         */
        workflows?: number;
        /**
         * Number of dashboards extracted
         */
        dashboards?: number;
        /**
         * Number of flows extracted
         */
        flows?: number;
    };
};
export namespace SchemaExtractionResponse {
    /**
     * Status of the extraction process
     */
    export enum status {
        COMPLETED = 'completed',
        IN_PROGRESS = 'in_progress',
        FAILED = 'failed',
    }
}

