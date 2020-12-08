import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http'
import { Cliente } from 'src/app/users/Cliente';
@Injectable({
  providedIn: 'root'
})
export class SignUpService {

  private url:string; ;
  constructor(private _http:HttpClient) { 
    this.url ='http://localhost:8080/signUp';
  }

  saveSignUp(client: Cliente){
    const headers = new HttpHeaders({ 'Access-Control-Allow-Origin:': "*" , 
    "Access-Control-Allow-Methods " : "POST, GET, OPTIONS, DELETE, PUT",
    "Access-Control-Allow-Headers": "*"});
    const options = { headers: headers };
    return this._http.post<Cliente>(this.url, client);

  }
}
