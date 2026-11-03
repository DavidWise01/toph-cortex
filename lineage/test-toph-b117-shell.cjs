#!/usr/bin/env node
'use strict';
const assert=require('node:assert/strict');
const {SCALE,topHShell,scaledPosition}=require('./toph-b117-shell.cjs');
const x=topHShell();
assert.equal(SCALE,0.67);
assert.equal(x.outer,0.67);
assert.ok(Math.abs(x.inner-0.2144)<1e-14);
assert.ok(Math.abs(x.area_ratio-0.4489)<1e-14);
assert.ok(Math.abs(x.reference_volume_ratio-0.300763)<1e-14);
assert.equal(x.center,'VOID_|||0|||');
assert.deepEqual(x.nested_bands,[24,12,8,4,3,2,1,1]);
assert.deepEqual(scaledPosition({x:1,y:0,z:0}),{x:0.67,y:0,z:0});
assert.throws(()=>topHShell({outer:1,inner:1}),/Invalid/);
console.log('PASS TOPH B117: 67/100 linear girth, hollow core, scaled bands');
