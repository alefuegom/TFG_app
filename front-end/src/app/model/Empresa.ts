import { Usuario } from "./Usuario";

export interface Empresa{
    nombre:string;
    cif:string;
    direccion:string;
    telefono: BigInt;
    cuentaBancaria:string;
    usuario:Usuario;
}