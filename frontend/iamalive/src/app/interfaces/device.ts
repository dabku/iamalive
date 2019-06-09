import { IToken } from '../services/authentication.service';

export enum State {
    OK = 'OK',
    THRESHOLD = 'THRESHOLD',
    OK_TIMEOUT = 'OK TIMEOUT',
    THRESHOLD_TIMEOUT = 'THRESHOLD_TIMEOUT',
    TIMEOUT = 'TIMEOUT'
}


export interface IProperty {
    path: [string];
    value: IPropertyValue;
    state: State;
}

export interface IPropertyValue {
    value: number;
    threshold: number;
    timestamp: number;
}

export interface IStatus {
    value: number;
    timestamp: number;
    minimum_update_rate: number;
}

export interface ITokenData {
    token: string;
    expiry: number;
}

export interface IPropertyDetails {
    threshold: number;
    timeout: number;
    ok: number;

}

export interface IDevice {
    name: string;
    description: string;
    parent: string;
    status: IStatus;
    token: IToken;
    properties: IProperty[];
    propertyDetails: IPropertyDetails;
}
