import { Injectable } from '@angular/core';

import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ConnectionstateService {

  private pingUrl = '/api/v1/ping';
  public connectionState: boolean;

  constructor(private http: HttpClient) { }


  /** GET heroes from the server */
  getConnectionState(): Observable<IPongMessage> {
    return this.http.get<any>(this.pingUrl)
      .pipe(
        catchError(this.handleError('getConnectionState', []))
      );
  }
  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(error); // log to console instead
      return of({} as T);
    };
  }
}

export interface IPongMessage {
  message: string;
}
