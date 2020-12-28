import { EstadoServicio } from "./EstadoServicio";
import { EstadoSolicitud } from "./EstadoSolicitud";
import { Factura } from "./Factura";
import { SolicitudServicio } from "./SolicitudServicio";
import { Trabajador } from "./Trabajador";

export interface Servicio{
    id:number;
    estado:EstadoServicio;
    observaciones:string;
    solicitudServicio:SolicitudServicio;
    factura:Factura;
    trabajador:Trabajador;


}