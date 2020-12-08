import { Component, OnInit } from '@angular/core';
import {FormsModule} from '@angular/forms'
import { Router } from '@angular/router';
import { Cliente } from 'src/app/users/Cliente';
import { SignInService } from 'src/app/Service/sign-in/sign-in.service';

@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.css'],
  providers:[SignInService]

})
export class SignInComponent implements OnInit {

  constructor( private router:Router, private signInService: SignInService) { }
  userModel = new Cliente('Mike', 'White', '12345678S',123456789, 'Hellow word', 'mikeWhite@a.es','hello','None');

  ngOnInit(): void {
  }

  onSubmit(){
    this.signInService.signIn(this.userModel).subscribe(
      data=> console.log('Success!', data), 
      error => console.log('Error !', error)
    );
    this.router.navigate(['signUp']);
  }

}
