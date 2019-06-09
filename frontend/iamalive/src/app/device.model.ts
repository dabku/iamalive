import { Property } from './property.model';
import {IStatus, ITokenData, IPropertyDetails, State, IDevice} from './interfaces/device';



export class Device {
    public name: string;
    description: string;
    parent: string;
    password: string;
    private status: IStatus = {
        value: 0,
        timestamp: 0,
        minimum_update_rate: 0,
    };
    tokenData: ITokenData;
    properties: Property[];
    propertyDetails: IPropertyDetails;

    constructor(deviceResponse: IDevice) {
        this.propertyDetails = {
            threshold: 0,
            timeout: 0,
            ok: 0,
         };

        this.name = deviceResponse.name;
        this.status = deviceResponse.status;
        this.description = deviceResponse.description;

        const propertiesArray = deviceResponse.properties.map(property => {
                return new Property(property, this.status.minimum_update_rate);
            });
        this.properties = propertiesArray;
        for (const prop of propertiesArray) {
            if (prop.state === State.OK) {
                this.propertyDetails.ok += 1;
            } else if (prop.state === State.THRESHOLD) {
                this.propertyDetails.threshold += 1;
            } else {
                this.propertyDetails.timeout += 1;
            }
        }
    }

    getStatus() {
        const timestamp = new Date().getTime() / 1000;
        if (this.status.timestamp + this.status.minimum_update_rate < timestamp) {
            return this.status.value + ' TIMEOUT';
        }
        if (this.status.value) {
            return this.status.value;
        }
    }
}


