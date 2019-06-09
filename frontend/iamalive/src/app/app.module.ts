import { BrowserModule } from '@angular/platform-browser';
import { NgModule, InjectionToken } from '@angular/core';
import { HttpClientModule, HTTP_INTERCEPTORS  } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { DevicesComponent } from './devices/devices.component';
import { DeviceDetailComponent } from './device-detail/device-detail.component';
import { ConnectionstateComponent } from './connectionstate/connectionstate.component';
import { AuthenticationComponent } from './authentication/authentication.component';
import { HttpInterceptorService } from './interceptors/httpheaderinterceptor';
import { ApiUrlInterceptor, API_URL } from './interceptors/apiurlinterceptor';

import {environment } from '../environments/environment';


@NgModule({
  declarations: [
    AppComponent,
    DevicesComponent,
    DeviceDetailComponent,
    ConnectionstateComponent,
    AuthenticationComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
  ],
  providers: [
    {provide: API_URL, useValue: environment.api_url},
    {provide: HTTP_INTERCEPTORS, useClass: HttpInterceptorService, multi: true},
    {provide: HTTP_INTERCEPTORS, useClass: ApiUrlInterceptor, multi: true},
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
