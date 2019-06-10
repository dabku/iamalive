import {HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';

@Injectable()
export class HttpInterceptorService implements HttpInterceptor {

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const token = localStorage.getItem('currentUserToken');
    if (token) {
        request = request.clone({headers: request.headers.set('Authorization', 'Bearer ' + token)});
    }
    request = request.clone({headers: request.headers.set('Access-Control-Allow-Origin', '*' )});
    request = request.clone({headers: request.headers.set('Access-Control-Allow-Methods', 'GET, POST, DELETE, PUT' )});
    return next.handle(request);
  }
}
