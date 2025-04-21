/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type ApexTestResult = {
    apexClass?: string;
    outcome?: ApexTestResult.outcome;
    message?: string;
    stackTrace?: string;
    testDuration?: number;
    testStartTime?: string;
    testEndTime?: string;
    testRunId?: string;
    testRunStatus?: ApexTestResult.testRunStatus;
    testRunMessage?: string;
    testRunStackTrace?: string;
    testRunDuration?: number;
    testRunStartTime?: string;
    testRunEndTime?: string;
};
export namespace ApexTestResult {
    export enum outcome {
        PASSED = 'Passed',
        FAILED = 'Failed',
        SKIPPED = 'Skipped',
    }
    export enum testRunStatus {
        PASSED = 'Passed',
        FAILED = 'Failed',
        SKIPPED = 'Skipped',
    }
}

