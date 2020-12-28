import { Usuario } from "./Usuario";

export interface Persona{
    nombre:string;
    apellidos:string;
    dni:string;
    telefono:number;
    usuario:Usuario;    
}