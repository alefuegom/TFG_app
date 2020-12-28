import { Persona } from "./Persona";
import { Vehiculo } from "./Vehiculo";

export interface Trabajador{
    cualificacion:string;
    persona:Persona;
    vehiculo:Vehiculo;
    
}