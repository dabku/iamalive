import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthenticationService } from '../services/authentication.service';

@Component({
  selector: 'app-authentication',
  templateUrl: './authentication.component.html',
  styleUrls: ['./authentication.component.css']
})



export class AuthenticationComponent implements OnInit {
  loginForm: FormGroup;
  submitted = false;
  loading = false;
  message: string;

  constructor(private formBuilder: FormBuilder,
              private authenticationService: AuthenticationService,
              private router: Router) { }


  ngOnInit() {

    this.loginForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
  });
  }
  get f() { return this.loginForm.controls; }

  onSubmit() {
    this.submitted = true;
    if (this.loginForm.invalid) {
        return;
    }

    this.loading = true;
    this.authenticationService.login(this.loginForm.controls.username.value, this.loginForm.controls.password.value)
        .pipe()
        .subscribe(
            data => {
              this.router.navigate(['/']);
            },
            error => {
                this.message = LogMessages.authFailed;
                this.loading = false;
            });
}

}
export enum LogMessages
{
  authFailed = 'Authorization Failed'
}