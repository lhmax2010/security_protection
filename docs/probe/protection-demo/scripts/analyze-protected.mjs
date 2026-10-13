import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
const root = process.env.PROBE_ROOT;
const base = path.join(root, 'docs/probe/protection-demo');
const target = path.join(base, 'bin/target_c_llvm_armv7l_protected');
const dir = path.join(base, 'protected');
fs.mkdirSync(dir, {recursive:true});
const {Client} = await import(path.join(root, '.local-tools/rea/node_modules/@modelcontextprotocol/client/dist/index.mjs'));
const {StdioClientTransport} = await import(path.join(root, '.local-tools/rea/node_modules/@modelcontextprotocol/client/dist/stdio.mjs'));
const client = new Client({name:'protection-demo',version:'1.0.0'});
const transport = new StdioClientTransport({
  command:path.join(root,'.local-tools/node-v24.21.0-linux-x64/bin/node'),
  args:[path.join(root,'.local-tools/rea/node_modules/rea-agents/scripts/rea.mjs'),'mcp'],
  env:{...process.env},stderr:'pipe'});
transport.stderr?.on('data', d => fs.appendFileSync(path.join(dir,'mcp-stderr.txt'),d));
const save = (label,value) => fs.writeFileSync(path.join(dir,label+'.json'),JSON.stringify(value,null,2)+'\n');
const records = [];
async function call(label,tool,args={}) {
  const start = Date.now();
  let response;
  try { response = await client.callTool({name:tool,arguments:args},undefined,{timeout:600000}); }
  catch(e) { response = {transport_error:{name:e.name,message:e.message,code:e.code,data:e.data}}; }
  save(label,response);
  let value = response.structuredContent;
  if (!value) for (const c of response.content||[]) if(c.type==='text') {
    try {value=JSON.parse(c.text);break;} catch {}
  }
  if(value) save(label+'.decoded',value);
  records.push({label,tool,arguments:args,elapsed_ms:Date.now()-start,
    isError:!!response.isError,transport_error:response.transport_error||null});
  save('requests',records);
  console.log(label,records.at(-1).elapsed_ms+'ms');
  if(response.isError || response.transport_error || value?.status==='error' || value?.error)
    throw new Error(JSON.stringify(response));
  return value;
}
let opened = false;
try {
  await client.connect(transport);
  save('server-version',client.getServerVersion());
  save('target-identity',{path:target,sha256:crypto.createHash('sha256').update(fs.readFileSync(target)).digest('hex')});
  await call('open','open_binary',{path:target,provider_id:'ghidra'}); opened=true;
  const overview=await call('overview','binary_overview');
  await call('function-search','search_procedures',{pattern:'secret_transform'});
  await call('marker-search','search_strings',{pattern:'LICENSE_KEY_CHECK_V1'});
  const procedures=await call('procedures','list_procedures');
  const strings=await call('strings','list_strings');
  const sections=execFileSync(path.join(root,'.local-tools/sysroot/usr/bin/arm-linux-gnueabihf-readelf'),['-SW',target],{encoding:'utf8'});
  fs.writeFileSync(path.join(dir,'elf-sections.txt'),sections);
  const elfText=parseInt(sections.match(/\]\s+\.text\s+\S+\s+([0-9a-f]+)/i)[1],16);
  const ghidraText=Number.parseInt(overview.normalized_result.segments.find(s=>s.name==='.text').start,16);
  const relocation=ghidraText-elfText;
  const ground=JSON.parse(fs.readFileSync(path.join(base,'function-addresses.json')));
  const mapped={method:ground.method,elf_text:elfText,ghidra_text:ghidraText,relocation,functions:{}};
  for(const name of ['secret_transform','simple_checksum','main']) {
    const address='0x'+(parseInt(ground.functions[name].elf_value,16)+relocation).toString(16);
    mapped.functions[name]={address,ground_truth:ground.functions[name]};
    await call(name+'-info','procedure_info',{procedure:address});
    const pseudo=await call(name+'-pseudocode','procedure_pseudo_code',{procedure:address});
    fs.writeFileSync(path.join(dir,name+'-pseudocode.c'),pseudo.normalized_result);
    await call(name+'-assembly','procedure_assembly',{procedure:address});
    await call(name+'-callers','procedure_callers',{procedure:address});
  }
  save('address-provenance',mapped);
  const rows=procedures.normalized_result;
  const local=rows.filter(x=>!x.procedure?.external&&!x.procedure?.thunk);
  save('symbol-string-statistics',{
    method:'Projection of complete REA procedures/strings responses; Ghidra labels are not original-name recovery rates',
    procedure_rows:rows.length,local_non_thunk:local.length,
    local_FUN_labels:local.filter(x=>x.value.startsWith('FUN_')).length,
    secret_transform_named_rows:rows.filter(x=>x.value.includes('secret_transform')).length,
    string_rows:strings.normalized_result.length,string_samples:strings.normalized_result.slice(0,10)});
} finally {
  if(opened) await call('close','close_binary');
  await client.close();
}
