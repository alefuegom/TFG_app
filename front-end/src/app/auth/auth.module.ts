import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AuthRoutingModule } from './auth-routing.module';
import { LoginComponent } from './components/login/login.component';
import { RegistroComponent } from './components/registro/registro.component';
import { RouterModule } from '@angular/router';


@NgModule({
  declarations: [LoginComponent, RegistroComponent],
  imports: [
    CommonModule,
    AuthRoutingModule, 
    RouterModule
  ],
  exports:[
    LoginComponent, RegistroComponent
  ]    
  
})
export class AuthModule { }
