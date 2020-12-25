import { Usuario } from "./Usuario";

export class Empresa{
    nombre:string;
    cif:string;
    direccion:string;
    telefono: BigInt;
    cuentaBancaria:string;
    usuario:Usuario;

    constructor(nombre:string, cif:string, direccion:string, 
        telefono:BigInt, cuentaBancaria:string, usuario:Usuario){}
}