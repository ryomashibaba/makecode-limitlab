// G4-C7 A49 — G0 image-first spatial concepts; SVG IS NOT real geometry or evidence of walkability.
// Two competing compositional directions, each section + far-view massing panel.
// Node: node tools/g4c7_a49_g0_concepts.mjs --write
import fs from "node:fs";
import path from "node:path";
const C={bg:"#F5F2EA",paper:"#FFFEF9",ink:"#1A2D35",muted:"#526872",hair:"#C5CFCE",stone:"#9EABA7",shadow:"#485E67",market:"#DC925D",culture:"#D66A61",reading:"#418E99",home:"#85A981",route:"#EACB83",glass:"#C8E6DF",mark:"#E5E6DC"};
function r(x,y,w,h,c,rad=0,stroke="none",sw=1){return '<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="'+rad+'" fill="'+c+'" stroke="'+stroke+'" stroke-width="'+sw+'"/>';}
function poly(points,c,stroke="none",sw=1){return '<polygon points="'+points+'" fill="'+c+'" stroke="'+stroke+'" stroke-width="'+sw+'"/>';}
function path(d,c,stroke="none",sw=1,extra=""){return '<path d="'+d+'" fill="'+c+'" stroke="'+stroke+'" stroke-width="'+sw+'" '+extra+'/>';}
function line(a,b,c,d,color=C.ink,sw=2,extra=""){return '<line x1="'+a+'" y1="'+b+'" x2="'+c+'" y2="'+d+'" stroke="'+color+'" stroke-width="'+sw+'" '+extra+'/>';}
function txt(x,y,t,size=20,c=C.ink,weight="400"){return '<text x="'+x+'" y="'+y+'" font-family="Arial, Noto Sans JP, sans-serif" font-weight="'+weight+'" font-size="'+size+'" fill="'+c+'">'+t+'</text>';}
function person(x,y){return '<circle cx="'+x+'" cy="'+(y-18)+'" r="6" fill="'+C.ink+'"/>'+line(x,y-12,x,y+9,C.ink,3)+line(x,y+5,x-6,y+18,C.ink,2)+line(x,y+5,x+6,y+18,C.ink,2);}
function frame(title,subtitle,body){
 let out='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1360 860" role="img" width="1360" height="860">';
 out+=r(0,0,1360,860,C.bg)+r(32,32,1296,796,C.paper,10,C.hair,2)+r(32,32,1296,102,C.ink);
 out+=txt(67,77,title,31,"#fff","700")+txt(68,111,subtitle,18,"#D6E6E2");
 out+=body;
 out+=r(32,787,1296,41,C.ink)+txt(67,813,"A49 · G0 ONLY  /  CONCEPTUAL 2D · NOT REAL 3D · ART HOLD · NO MINECRAFT CONSTRUCTION",16,"#F3F2E8");
 return out+"</svg>";
}
function grid(){let s="";for(let x=100;x<1260;x+=80)s+=line(x,155,x,733,C.hair,.6);for(let y=170;y<=731;y+=70)s+=line(83,y,1270,y,C.hair,.6);return s;}
function legend(){return [ ["Market",C.market],["Culture",C.culture],["Reading/Research",C.reading],["Residential",C.home]].map(([t,c],i)=>r(93+i*270,743,16,16,c,3)+txt(116+i*270,757,t,16,C.muted)).join("");}
function aSection(){
 let s=grid()+r(88,639,1186,67,C.mark,0);
 s+=path("M144 641 L208 456 L405 412 L537 364 L667 345 L782 291 L969 245 L1149 280 L1176 640 L1091 640 L1057 326 L950 314 L812 381 L722 433 L565 436 L425 487 L390 638 Z",C.shadow);
 // rooms modeled as solid deep-colored areas with real-looking space (but still only conceptual)
 s+=poly("176,631 176,486 382,449 441,492 441,631",C.market);
 s+=poly("402,622 422,448 589,388 749,412 724,577 596,622",C.culture);
 s+=poly("601,440 735,357 930,303 1036,334 1008,503 784,517",C.reading);
 s+=poly("775,335 921,275 1114,302 1120,421 986,421 926,369",C.home);
 // shared civic chamber carved out from the volumes, not empty immense plaza
 s+=path("M403 625 C465 543 524 513 601 520 Q677 509 721 472 L778 468 L751 637 Z",C.paper);
 // active interfaces, separate their projected occupied depth
 for(let x=209;x<=375;x+=48){s+=r(x,535,25,63,C.paper,2)+r(x,605,25,12,C.shadow);}
 for(let x=820;x<=1000;x+=49)s+=r(x,376,24,48,C.glass,3);
 for(let x=821;x<=1070;x+=43)s+=r(x,310,18,32,"#DCECDD",3);
 s+=path("M135 629 C242 608 315 611 395 605 S513 580 590 574 S716 549 784 511","none",C.route,13,'stroke-linecap="round"');
 s+=line(410,566,518,476,C.ink,2,'stroke-dasharray="8 8"')+line(410,566,835,414,C.ink,2,'stroke-dasharray="8 8"');
 for(let [x,y] of [[194,631],[342,631],[515,620],[653,617],[817,501]])s+=person(x,y);
 s+=txt(169,478,"M",34,C.paper,"700")+txt(498,402,"C",34,C.paper,"700")+txt(763,368,"R",34,C.paper,"700")+txt(999,291,"H",34,C.paper,"700");
 s+=r(92,170,286,95,C.ink,8)+txt(114,202,"A · DEEP ACTIVE",20,"#fff","700")+txt(114,230,"THRESHOLD SECTION",18,"#B7D8D2")+txt(114,250,"Activity first · shell later",15,"#fff");
 s+=txt(116,730,"Human viewpoint: from shared civic chamber to deep usable rooms (unverified)",17,C.ink,"600")+legend();
 return frame("A — INTERLOCKED CIVIC CHAMBERS / 交差する居住公共室","Public room + deep market/culture/reading/housing occupy the SAME thick urban section.",s);
}
function aDistance(){
 let s=grid()+r(87,646,1187,75,"#CED7D1");
 s+=poly("166,638 212,456 401,392 563,371 643,309 830,246 1090,306 1159,562 1048,641 869,564 759,581 570,523 420,632",C.shadow);
 s+=poly("212,456 397,390 565,369 641,309 828,249 1094,309 1049,352 830,306 656,380 561,438 408,466 265,517",C.stone);
 // windowed occupied portions in silhouette
 s+=poly("210,516 412,467 562,439 540,562 424,600 222,626",C.market);
 s+=poly("423,469 562,441 741,419 733,536 552,570 421,600",C.culture);
 s+=poly("656,381 833,311 1051,352 1013,516 866,541 750,504",C.reading);
 s+=poly("832,251 1095,307 1129,462 1048,442 1008,358 832,307",C.home);
 // merge public deep aperture
 s+=path("M418 640 Q474 528 591 519 Q683 506 739 557 L775 643 Z",C.paper);
 for(let i=0;i<7;i++)s+=r(243+i*40,508-i*10,20,37,C.glass,2);
 for(let i=0;i<5;i++)s+=r(820+i*43,379+i*7,23,44,C.glass,2);
 s+=path("M150 639 Q303 608 402 628 Q543 625 652 637","none",C.route,16,'stroke-linecap="round"');
 for(let [x,y] of [[222,639],[340,638],[481,640],[625,641]])s+=person(x,y);
 s+=r(93,169,383,103,C.ink,8)+txt(116,205,"MASSING CONTRACT — A",22,"#fff","700")+txt(116,236,"NOT a rendering / not city-scale pass",17,"#D1E5DE");
 s+=txt(788,728,"One architectural address · occupied depth must remain legible",19,C.ink,"600");
 s+=legend();
 return frame("A — LONG-VIEW MASSING HYPOTHESIS / 遠景の主建築仮説","Asymmetric one-body silhouette. Visible rooms and an open civic cut must stay related.",s);
}
function bSection(){
 let s=grid()+r(88,638,1188,66,C.mark);
 s+=poly("139,636 176,433 306,304 507,355 557,629",C.shadow);
 s+=poly("712,633 777,419 961,282 1147,357 1200,635",C.shadow);
 s+=poly("178,433 308,305 501,357 485,405 311,370 216,489",C.stone);
 s+=poly("783,418 961,282 1149,357 1135,422 968,357 839,480",C.stone);
 s+=poly("196,627 237,503 314,413 490,441 480,626",C.market);
 s+=poly("795,616 827,489 969,396 1127,432 1171,626",C.reading);
 s+=poly("460,475 807,429 857,454 535,526",C.culture);
 s+=poly("291,350 399,369 482,411 469,463 302,419",C.home);
 s+=path("M540 620 L536 527 L850 463 L854 630 Z",C.paper);
 // bridge is central character and looks like already rejected typology
 s+=path("M477 474 L824 419 L843 459 L518 530 Z",C.stone);
 s+=path("M157 631 C295 610 467 626 545 637 L1054 640","none",C.route,11,'stroke-linecap="round"');
 for(let x=0;x<5;x++)s+=r(271+x*37,478,17,34,C.glass,2);
 for(let x=0;x<5;x++)s+=r(875+x*42,446,17,42,C.glass,2);
 for(let [x,y] of [[219,629],[483,624],[820,621],[1050,629]])s+=person(x,y);
 s+=r(93,166,385,115,C.ink,8)+txt(113,200,"B · SPLIT OCCUPIED BANKS",22,"#fff","700")+txt(113,232,"Culture bridge above empty void",18,"#D2E4DB")+txt(113,255,"Clear recurrence risk: quarry + bridge",16,C.paper);
 s+=txt(564,580,"UNPROGRAMMED VOID",22,C.ink,"700");
 s+=txt(116,730,"Looks connected as a drawing — still two buildings plus a bridge",18,C.ink,"600")+legend();
 return frame("B — OCCUPIED BANKS + BRIDGE / 双岸文化架橋","Distinct alternative: separated inhabitable banks linked by a central cultural span.",s);
}
function bDistance(){
 let s=grid()+r(90,650,1184,61,"#CAD5CF");
 s+=poly("135,635 179,437 307,317 505,383 552,637",C.shadow)+poly("726,637 788,432 953,280 1133,376 1186,635",C.shadow);
 s+=poly("179,437 307,317 504,383 493,425 311,367 214,489",C.stone);
 s+=poly("792,431 951,282 1133,377 1156,438 954,362 835,491",C.stone);
 s+=poly("197,527 313,420 489,471 497,625 181,635",C.market);
 s+=poly("819,482 961,375 1146,445 1171,625 785,626",C.reading);
 s+=poly("478,471 804,408 868,474 534,555",C.culture);
 s+=path("M506 558 L850 493 L805 561 L543 598 Z",C.stone);
 s+=path("M541 638 L541 596 L805 560 L815 638 Z",C.paper);
 for(let i=0;i<5;i++)s+=r(243+i*42,493-i*5,19,29,C.glass,2);
 for(let i=0;i<5;i++)s+=r(882+i*42,476+i*3,20,36,C.glass,2);
 for(let [x,y] of [[240,639],[476,636],[851,636],[1080,638]])s+=person(x,y);
 s+=r(92,170,392,105,C.ink,8)+txt(115,204,"MASSING RISK — B",22,C.paper,"700")+txt(115,235,"Pavilion + bridge is not a megacity",17,"#D1E5DE");
 s+=txt(554,744,"Split skyline — coherent architecture remains unproven",18,C.ink,"600")+legend();
 return frame("B — LONG-VIEW MASSING RISK / 遠景の分離リスク","The bridge draws attention to the gap, bringing back A39/A42-type separation.",s);
}
const drawings={"01_A_OCCUPIED_SECTION.svg":aSection(),"02_A_OUTSIDE_CONTRACT.svg":aDistance(),"03_B_BANKS_SECTION.svg":bSection(),"04_B_SPLIT_OUTSIDE.svg":bDistance()};
function validate(name,source){const roots=(source.match(/<svg\b/g)||[]).length,closed=(source.match(/<\/svg>/g)||[]).length;return {name,characters:source.length,rootCount:roots,closeCount:closed,svgNamespace:source.includes('xmlns="http://www.w3.org/2000/svg"'),containsHold:source.includes("ART HOLD"),clearlyConcept:source.includes("NOT REAL 3D"),containsScripts:/<script/i.test(source),externalLinks:/<image\b|href\s*=/i.test(source)};}
function run(){let checks=Object.entries(drawings).map(([n,s])=>validate(n,s));if(checks.some(x=>x.rootCount!==1||x.closeCount!==1||!x.svgNamespace||!x.containsHold||!x.clearlyConcept||x.containsScripts||x.externalLinks))throw Error("invalid SVG contract");const dir="artifacts/g4c7-a49-preflight";if(process.argv.includes("--write")){for(let n of Object.keys(drawings))if(fs.existsSync(path.join(dir,n)))throw Error("Refusing to overwrite "+n);fs.mkdirSync(dir,{recursive:true});for(let [n,s]of Object.entries(drawings))fs.writeFileSync(path.join(dir,n),s);}console.log(JSON.stringify(checks));}
if(process.argv.includes("--write")||process.argv.includes("--check"))run();
export {drawings,validate};
