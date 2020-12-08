import { Component, OnInit } from '@angular/core';
import {FormsModule} from '@angular/forms'
import { Cliente } from 'src/app/users/Cliente';
import {SignUpService} from 'src/app/Service/sign-up/sign-up.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css'],
  providers:[SignUpService]
})
export class SignUpComponent implements OnInit {

  constructor( private router:Router, private signUpService: SignUpService) { }
  userModel = new Cliente('Mike', 'White', '12345678S',123456789, 'Hellow word', 'mikeWhite@a.es','hello','None');
  ngOnInit(): void {
  }
  onSubmit(){
    this.signUpService.saveSignUp(this.userModel).subscribe(
      data=> console.log('Success!', data), 
      error => console.log('Error !', error)
    );
    this.router.navigate(['signIn']);
  }

}
