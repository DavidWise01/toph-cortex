#!/usr/bin/env node
'use strict';
const A=require('node:assert/strict'),K=require('./toph-b001-frustule.cjs');
const a=K.cells({scale:1}),b=K.cells();
A.equal(a.length,60);A.equal(b.length,60);
A.deepEqual(K.verify().total,60);A.equal(b.filter(x=>x.isCore).length,20);
for(let i=0;i<a.length;i++){
 for(const ax of ['x','y','z','siteRadius'])A.ok(Math.abs(b[i][ax]-a[i][ax]*.67)<1e-10);
 A.equal(a[i].channel,b[i].channel);A.equal(a[i].layer,b[i].layer);
}
A.equal(K.sector(120),'Ice');A.equal(K.sector(240),'Ag');
A.equal(K.sector(360),'Au');
A.equal(K.foldPoint(b[0],0).y,b[0].y);
A.throws(()=>K.cells({scale:0}),/Invalid/);
console.log('PASS: TOPH B001 60 cells / 10 layers / 20 core, exact 67% geometry, channel and topology preservation');
