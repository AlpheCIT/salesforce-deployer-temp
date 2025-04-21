/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type SchemaComparisonResponse = {
    differences: Array<{
        componentType: 'object' | 'field' | 'workflow' | 'dashboard' | 'flow';
        componentName: string;
        changeType: 'added' | 'removed' | 'modified';
        sourcePath?: string;
        targetPath?: string;
        /**
         * Component value in the source schema
         */
        sourceValue?: Record<string, any>;
        /**
         * Component value in the target schema
         */
        targetValue?: Record<string, any>;
        /**
         * Field-level changes (for modified components)
         */
        fieldChanges?: Array<{
            field: string;
            changeType: 'added' | 'removed' | 'modified';
            sourceValue?: Record<string, any>;
            targetValue?: Record<string, any>;
        }>;
    }>;
};

