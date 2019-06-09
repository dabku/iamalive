import { IProperty, IPropertyValue, State } from './interfaces/device';

export class Property {
    path: [string];
    value: IPropertyValue = {
        value: 0,
        threshold: 0,
        timestamp: 0
    };

    state: State;


    constructor(property, timeoutPeriod) {
        const timestamp = new Date().getTime() / 1000;
        this.path = property[0];
        this.value = property[1];

        this.state = this.value.value < this.value.threshold ? State.OK : State.THRESHOLD;

        if (this.value.timestamp + timeoutPeriod < timestamp) {
            (this.state as any) += ' TIMEOUT';
        }

    }
    getPath() {
        return this.path.join(' > ');
    }
}

