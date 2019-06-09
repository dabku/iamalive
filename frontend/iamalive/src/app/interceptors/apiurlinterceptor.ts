import {HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';
import {Injectable, Inject, InjectionToken} from '@angular/core';
import {Observable} from 'rxjs';




export const API_URL = new InjectionToken<string>('api_url');

@Injectable()
export class ApiUrlInterceptor implements HttpInterceptor {

private apiUrl: string;

constructor(@Inject(API_URL) apiUrl) {
    this.apiUrl = apiUrl;
}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    req = req.clone({url: this.prepareUrl(req.url)});
    return next.handle(req);
  }

  private isAbsoluteUrl(url: string): boolean {
    const absolutePattern = /^https?:\/\//i;
    return absolutePattern.test(url);
  }

  private isApi(url: string): boolean {
    const apiPattern = /\/api\//;
    return apiPattern.test(url);
  }

  private prepareUrl(url: string): string {
      if (!this.isApi(url)) {
          return url;
      }
      url = this.isAbsoluteUrl(url) ? url : this.apiUrl + '/' + url;
      return url.replace(/([^:]\/)\/+/g, '$1');
  }
}
