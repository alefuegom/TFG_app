import { ɵPlayerFactory } from "@angular/core";
import { Cliente } from "./Cliente";
import { Empresa } from "./Empresa";
import { EstadoSolicitud } from "./EstadoSolicitud";
import { Plaga } from "./Plaga";
import { Tratamiento } from "./Tratamiento";

export interface SolicitudServicio{
    id: number;
    estado:EstadoSolicitud;
    fecha:Date;
    observaciones:string;
    cliente:Cliente;
    empresa:Empresa;
    tratamiento:Tratamiento;
    plaga:Plaga;

}