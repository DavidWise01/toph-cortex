'use strict';
// B117 TOPH daughter geometry: exact rational 67/100 of Grandma's LINEAR girth.
// This module is only geometry; it does not start a computational agent.
const G_NUM=67n,G_DEN=100n;
const SCALE=Number(G_NUM)/Number(G_DEN);
function topHShell(grandma={outer:1,inner:0.32}){
 const outer=Number(grandma.outer),inner=Number(grandma.inner);
 if(!(Number.isFinite(outer)&&Number.isFinite(inner)&&outer>0&&inner>=0&&inner<outer))throw Error('Invalid hollow Grandma shell');
 return Object.freeze({
  relationship:'FIRST_DAUGHTER',
  inherited_linear_girth:'67/100',
  outer:outer*SCALE,
  inner:inner*SCALE,
  thickness:(outer-inner)*SCALE,
  circumference_ratio:SCALE,
  area_ratio:SCALE*SCALE,
  reference_volume_ratio:SCALE*SCALE*SCALE,
  center:'VOID_|||0|||',
  nested_bands:[24,12,8,4,3,2,1,1]
 });
}
function scaledPosition(p){return {x:p.x*SCALE,y:p.y*SCALE,z:p.z*SCALE}}
module.exports={SCALE,topHShell,scaledPosition};
