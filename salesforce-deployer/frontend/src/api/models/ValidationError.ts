/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type ValidationError = {
    message: string;
    severity?: ValidationError.severity;
    componentType?: string;
    componentName?: string;
    path?: string;
};
export namespace ValidationError {
    export enum severity {
        ERROR = 'error',
        WARNING = 'warning',
        INFO = 'info',
    }
}

