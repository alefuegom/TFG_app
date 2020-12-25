import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import { Cliente } from 'src/app/model/Cliente';


@Injectable({
  providedIn: 'root'
})
export class SignInService {

  constructor(private http:HttpClient) { }

  url = 'http://localhost:8080/ProyectoTFG/signIn';

  signIn(client: Cliente){
    const headers = new HttpHeaders({ 'Access-Control-Allow-Origin:': "*" });
    const options = { headers: headers };
    return this.http.post<any>(this.url, client);

  }


}
