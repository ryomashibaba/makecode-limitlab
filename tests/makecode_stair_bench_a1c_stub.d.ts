type Position = {x:number;y:number;z:number};
declare function world(x:number,y:number,z:number):Position;
declare const Axis:{X:number;Y:number;Z:number};
declare const player:{
 position():{getValue(axis:number):number};
 say(message:string):void;
 onChat(command:string,callback:()=>void):void;
};
declare const AIR:number;
declare const STONE:number;
declare const FillOperation:{Replace:number};
declare const blocks:{
 testForBlock(block:number,at:Position):boolean;
 fill(block:number,from:Position,to:Position,operation:number):void;
 place(block:number,at:Position):boolean;
 blockWithData(block:number,data:number):number;
};
declare const loops:{pause(ms:number):void};
