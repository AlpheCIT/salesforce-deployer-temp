/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ValidationError } from './ValidationError';
export type SchemaValidationResponse = {
    /**
     * Whether the schema is valid
     */
    valid: boolean;
    /**
     * Validation errors (if any)
     */
    errors?: Array<ValidationError>;
    /**
     * Validation warnings
     */
    warnings?: Array<ValidationError>;
    /**
     * Graph of component dependencies
     */
    dependencyGraph?: Record<string, Array<string>>;
};

