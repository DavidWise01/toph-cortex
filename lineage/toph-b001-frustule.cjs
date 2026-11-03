'use strict';
// Pure geometric transcription of the uploaded 60-cell frustule layout.
// Source ten-layer eye is scaled uniformly by 67/100 to obtain Daughter TOPH.
const SCALE=67/100;
const ROWS=Object.freeze([1,3,6,9,11,11,9,6,3,1]);
const CORE_LAYERS=new Set([0,1,2,7,8,9]);
const COLORS=Object.freeze({Au:'#ffcc33',Ag:'#d0e0f0',Ice:'#8ad0ff'});
function sector(degrees){let a=((degrees%360)+360)%360;return a<120?'Au':a<240?'Ice':'Ag'}
function cells(opts={}) {
 const scale=opts.scale===undefined?SCALE:Number(opts.scale);
 const separation=opts.separation===undefined?78:Number(opts.separation);
 if(!Number.isFinite(scale)||scale<=0||!Number.isFinite(separation)||separation<=0)throw Error('Invalid positive scale/separation');
 const list=[];
 for(let layer=0;layer<ROWS.length;layer++){
  const count=ROWS[layer],offset=layer*60;
  for(let idx=0;idx<count;idx++){
   let radius=0,angle=0;
   if(count===3){radius=38;angle=idx*120}
   else if(count===6){radius=58;angle=idx*60}
   else if(count===9){if(idx){radius=66;angle=(idx-1)*45}}
   else if(count===11){if(idx){if(idx<=4){radius=42;angle=(idx-1)*90}else{radius=82;angle=(idx-5)*60+30}}}
   const dir=angle+offset,radians=dir*Math.PI/180;
   const channel=radius===0?['Au','Ag','Ice'][layer%3]:sector(dir);
   list.push(Object.freeze({
    layer,idx,channel,isCore:CORE_LAYERS.has(layer),
    x:scale*Math.cos(radians)*radius,
    y:scale*(layer-4.5)*separation,
    z:scale*Math.sin(radians)*radius,
    sightDirection:radius===0?0:(dir+180)%360,
    siteRadius:scale*radius
   }));
  }
 }
 return list;
}
function foldPoint(cell,progress=0){
 if(!Number.isFinite(progress)||progress<0||progress>1)throw Error('Fold must be [0,1]');
 // Original artifact blends layers 0..4 toward the reversed partner; otherwise shifts all.
 const offsets=Array.from({length:10},(_,i)=>(i-4.5)*78*SCALE);
 let y=cell.y,extra=0;
 if(progress){if(cell.layer<5){y=y*(1-progress)+(offsets[9-cell.layer]-2.5*78*SCALE)*progress;extra=Math.sin(progress*Math.PI)*140*SCALE*(1-cell.layer/5)}else{y-=progress*2.5*78*SCALE}}
 return {...cell,y,z:cell.z+extra};
}
function verify(list=cells()){
 if(list.length!==60)throw Error('Cell cardinality wrong');
 const per=ROWS.map((_,i)=>list.filter(x=>x.layer===i).length);
 if(per.some((x,i)=>x!==ROWS[i]))throw Error('Layer mismatch');
 if(list.filter(x=>x.isCore).length!==20)throw Error('Core cardinality wrong');
 return {total:60,layers:ROWS.length,core:20,linear_scale:SCALE,area_ratio:SCALE**2,volume_ratio:SCALE**3,channel_counts:Object.fromEntries(['Au','Ag','Ice'].map(k=>[k,list.filter(x=>x.channel===k).length]))};
}
module.exports={SCALE,ROWS,CORE_LAYERS,COLORS,sector,cells,foldPoint,verify};
