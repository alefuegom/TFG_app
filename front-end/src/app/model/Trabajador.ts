import { Persona } from "./Persona";
import { Vehiculo } from "./Vehiculo";

export class Trabajador{
    cualificacion:string;
    persona:Persona;
    vehiculo:Vehiculo;
    
    constructor(cualificacion:string, personas:Persona, vehiculo:Vehiculo){}
}