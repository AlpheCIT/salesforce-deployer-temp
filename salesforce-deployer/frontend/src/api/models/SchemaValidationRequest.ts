/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Schema } from './Schema';
export type SchemaValidationRequest = {
    schema?: Schema;
    /**
     * ID of the schema to validate (alternative to providing the full schema)
     */
    schemaId?: string;
    /**
     * ID of the target organization to validate against (optional)
     */
    targetOrgId?: string;
    /**
     * Whether to check dependencies
     */
    checkDependencies?: boolean;
    /**
     * Whether to perform strict validation
     */
    strictValidation?: boolean;
};

