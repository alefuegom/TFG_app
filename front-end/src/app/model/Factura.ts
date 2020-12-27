export class Factura{
    numeroFactura: Int16Array;
    fechaExpedición: Date;
    emisor:string;
    receptor:string;
    descripcion:string;
    importe:Int16Array;
    tipoImpositivo: Int16Array;
    fechaOperaciones: Date;

    constructor(numeroFactura:Int16Array, fechaExpedicion:Date, emisor:string, receptor:string,
        descripcion:string, importe:Int16Array, tipoImpositivo:Int16Array, fechaOperaciones:Date){}
}