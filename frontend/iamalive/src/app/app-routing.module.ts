import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { DevicesComponent} from './devices/devices.component';
import { AuthenticationComponent} from './authentication/authentication.component';
import { AuthGuard } from './guards/auth.guard';

const routes: Routes = [
  { path: '', redirectTo: '/devices', pathMatch: 'full' , canActivate: [AuthGuard]},
  { path: 'devices', component: DevicesComponent, canActivate: [AuthGuard] },
  { path: 'login', component: AuthenticationComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
