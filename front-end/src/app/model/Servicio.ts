import { EstadoServicio } from "./EstadoServicio";
import { EstadoSolicitud } from "./EstadoSolicitud";
import { Factura } from "./Factura";
import { SolicitudServicio } from "./SolicitudServicio";
import { Trabajador } from "./Trabajador";

export class Servicio{
    id:Int16Array;
    estado:EstadoServicio;
    observaciones:string;
    solicitudServicio:SolicitudServicio;
    factura:Factura;
    trabajador:Trabajador;

    constructor(id:Int16Array, estado: EstadoServicio, observaciones:string, solicitudServicio:SolicitudServicio,
        factura:Factura, trabajador:Trabajador){}
}