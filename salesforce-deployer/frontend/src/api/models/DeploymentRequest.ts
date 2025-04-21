/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Schema } from './Schema';
export type DeploymentRequest = {
    /**
     * ID of the schema to deploy
     */
    schemaId?: string;
    schema?: Schema;
    /**
     * ID of the target organization
     */
    targetOrgId: string;
    /**
     * List of components to deploy. If not provided, all components will be deployed.
     */
    components?: Array<string>;
    options?: {
        /**
         * Validate but don't deploy
         */
        checkOnly?: boolean;
        /**
         * Ignore validation warnings
         */
        ignoreWarnings?: boolean;
        /**
         * Run specified tests
         */
        runTests?: boolean;
        testLevel?: DeploymentRequest.testLevel;
        /**
         * Roll back on error
         */
        rollbackOnError?: boolean;
        /**
         * Purge on delete
         */
        purgeOnDelete?: boolean;
        /**
         * Auto-update package
         */
        autoUpdatePackage?: boolean;
    };
};
export namespace DeploymentRequest {
    export enum testLevel {
        NO_TEST_RUN = 'NoTestRun',
        RUN_SPECIFIED_TESTS = 'RunSpecifiedTests',
        RUN_LOCAL_TESTS = 'RunLocalTests',
        RUN_ALL_TESTS_IN_ORG = 'RunAllTestsInOrg',
    }
}

