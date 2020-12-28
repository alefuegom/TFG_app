export interface Factura{
    numeroFactura: number;
    fechaExpedición: Date;
    emisor:string;
    receptor:string;
    descripcion:string;
    importe:number;
    tipoImpositivo: number;
    fechaOperaciones: Date;
}