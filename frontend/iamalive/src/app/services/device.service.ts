import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { Device} from '../device.model';
import { IDevice } from '../interfaces/device';

@Injectable({
  providedIn: 'root'
})
export class DeviceService {
  private deviceUrl = '/api/v1/device';

  constructor(private http: HttpClient) { }

  getDevices(): Observable<Device[]> {
    const options = { params: new HttpParams().set('flatten', 'true') };
    return this.http.get<IDevice[]>(this.deviceUrl, options)
      .pipe(
        map((data: IDevice[]) => {
           return data.map((device: IDevice) => new Device(device));
          }
        ),
        catchError(this.handleError<any>('getDevices', []))
      );
  }


  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(error);
      return of({} as T);
    };
  }
}

export interface IDevice {
  name: string;
}
