import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
  public currentUser: string;
  private loginUrl = '/api/v1/authenticate';
  constructor(private http: HttpClient,
              private router: Router) {
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

      );
  }

  public logout() {
    localStorage.removeItem('currentUserToken');
    localStorage.removeItem('currentUser');
    this.currentUser = null;
    this.router.navigate(['/login']);
  }
}


export interface IToken {
  token: string;
}
