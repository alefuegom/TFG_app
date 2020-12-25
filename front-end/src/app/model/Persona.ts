import { Usuario } from "./Usuario";

export class Persona{
    nombre:string;
    apellidos:string;
    dni:string;
    telefono:BigInt;
    usuario:Usuario;

    constructor(nombre:string, apellidos:string, dni:string, telefono:BigInt, usuario:Usuario){}
    
}