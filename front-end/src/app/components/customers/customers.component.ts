import { Component, OnInit } from '@angular/core';
import {Router} from '@angular/router'
import { Cliente } from 'src/app/users/Cliente';
import {CustomersService} from '../../Service/customers.service'
@Component({
  selector: 'app-customers',
  templateUrl: './customers.component.html',
  styleUrls: ['./customers.component.css']
})
export class CustomersComponent implements OnInit {
  
  clientes:Cliente[]
  constructor(private service:CustomersService, private router:Router) { }

  ngOnInit(): void {
    this.service.listCustomers().subscribe(data=>{
      this.clientes=data;
    })
    

  }

}
