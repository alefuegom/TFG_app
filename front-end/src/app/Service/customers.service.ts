import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Cliente } from '../model/Cliente';

@Injectable({
  providedIn: 'root'
})
export class CustomersService {

  constructor(private http:HttpClient) { }

  Url = 'http://localhost:8080/administrator/customers';

  listCustomers(){
    return this.http.get<Cliente[]>(this.Url);
  }
}
