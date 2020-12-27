export class Tratamiento{
    nombre:string;
    descripcion:string;
    precio:Int16Array;
    abandono:boolean;
    horasAbandono:Int16Array;

    constructor(nombre:string, descripcion:string, precio:Int16Array, 
        abandono:boolean, horasAbandono:Int16Array){}
}