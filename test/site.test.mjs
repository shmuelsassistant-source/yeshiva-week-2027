import test from 'node:test'; import assert from 'node:assert'; import fs from 'node:fs'; import path from 'node:path';
const S=path.resolve(path.dirname(new URL(import.meta.url).pathname),'../site');
const html=fs.readFileSync(path.join(S,'index.html'),'utf8');
test('title and viewport',()=>{assert.match(html,/<title>Yeshiva Week 2027/);assert.match(html,/name="viewport" content="width=device-width/);});
test('core content present',()=>{for(const s of ['Westgate River Ranch','Okeechobee KOA','Hawks Cay','$660.87','$955.00','Jonathan Dickinson','Rejected options','Family board','Method, access limits']) assert.ok(html.includes(s),s);});
test('local assets exist',()=>{for(const f of ['styles.css','script.js','_worker.js','tab-site.json','yeshiva-week-2027-source.zip']) assert.ok(fs.existsSync(path.join(S,f)),f); for(const m of html.matchAll(/href="(evidence\/[^"]+)"/g)) assert.ok(fs.existsSync(path.join(S,m[1])),m[1]);});
test('no placeholders or private identifiers',()=>{assert.ok(!/lorem ipsum|TODO|\{\{/i.test(html));assert.ok(!/@gmail|reservation #|confirmation #/i.test(html));});
test('3/4 night toggle and labels',()=>{assert.match(html,/data-n="3"/);assert.match(html,/data-n="4"/);assert.ok(html.includes('exact-date quote')&&html.includes('indicative'));});
