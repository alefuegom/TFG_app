import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SignInComponent } from './components/sign-in/sign-in.component';
import { SignUpComponent } from './components/sign-up/sign-up.component';
import {HttpClientModule} from '@angular/common/http'
import {FormsModule} from '@angular/forms';
import { CustomersComponent } from './components/customers/customers.component'
import{CustomersService} from '../app/Service/customers.service';
import { HeaderComponent } from './components/visual/header/header.component';
import { FooterComponent } from './components/visual/footer/footer.component';
import { HomeComponent } from './components/visual/home/home.component'
@NgModule({
  declarations: [
    AppComponent,
    SignInComponent,
    SignUpComponent,
    CustomersComponent,
    HeaderComponent,
    FooterComponent,
    HomeComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule, 
    HttpClientModule
  ],
  providers: [CustomersService],
  bootstrap: [AppComponent]
})
export class AppModule { }
