import { Injectable, InjectionToken } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { Router} from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
  public currentUser: string;
  private loginUrl = '/api/v1/authenticate';
  constructor(private http: HttpClient,
              private router: Router ) {
                this.currentUser = localStorage.getItem('currentUser');
              }

  public login(username: string, password: string): Observable<IToken> {
    const options = { params: new HttpParams().set('username', username).set('password', password) };

    return this.http.get<IToken>(this.loginUrl, options)
      .pipe(map(data => {
        localStorage.setItem('currentUserToken', data.token);
        localStorage.setItem('currentUser', username);
        this.currentUser = username;
        return data;
      })
        // catchError(this.handleError('login', []))

      );
  }

  public logout() {
    localStorage.removeItem('currentUserToken');
    localStorage.removeItem('currentUser');
    this.currentUser = null;
    this.router.navigate(['/login']);
  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // Let the app keep running by returning an empty result.
      return of({} as T);
    };
  }
}


export interface IToken {
  token: string;
}
