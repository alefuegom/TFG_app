import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent {
  title = 'ProyectoTFG';
  constructor(private router:Router){}


  ngOnInit(): void {
  }
  signIn(){
    this.router.navigate(["signIn"]);
  }

  signUp(){
    this.router.navigate(["signUp"]);
  }

}
