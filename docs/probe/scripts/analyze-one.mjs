import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const root=process.env.PROBE_ROOT;
const {Client}=await import(path.join(root,'.local-tools/rea/node_modules/@modelcontextprotocol/client/dist/index.mjs'));
const {StdioClientTransport}=await import(path.join(root,'.local-tools/rea/node_modules/@modelcontextprotocol/client/dist/stdio.mjs'));
const [mode,name]=process.argv.slice(2);
const target=path.join(root,'docs/probe/samples/bin',name);
const dir=path.join(root,'docs/probe/evidence',name,...(mode==='followup'?['supplemental']:[]));fs.mkdirSync(dir,{recursive:true});
const client=new Client({name:'bare-baseline-audit',version:'1.0.0'});
const transport=new StdioClientTransport({command:path.join(root,'.local-tools/node-v24.21.0-linux-x64/bin/node'),args:[path.join(root,'.local-tools/rea/node_modules/rea-agents/scripts/rea.mjs'),'mcp'],env:{...process.env},stderr:'pipe'});
const records=[];
transport.stderr?.on('data',d=>fs.appendFileSync(path.join(dir,'mcp-stderr.txt'),d));
const save=(label,data)=>fs.writeFileSync(path.join(dir,label+'.json'),JSON.stringify(data,null,2)+'\n');
async function call(label,tool,args={}) {
 const start=Date.now();let response;
 try {response=await client.callTool({name:tool,arguments:args},undefined,{timeout:600000});}
 catch(e) {response={transport_error:{name:e.name,message:e.message,code:e.code,data:e.data}};}
 save(label,response);
 let value=response.structuredContent;
 if(!value)for(const c of response.content||[])if(c.type==='text'){try{value=JSON.parse(c.text);break;}catch{}}
 if(value)save(label+'.decoded',value);
 const record={label,tool,arguments:args,elapsed_ms:Date.now()-start,isError:response.isError||false,transport_error:response.transport_error||null};
 records.push(record);save('requests',records);console.log(label,record.elapsed_ms,record.isError,record.transport_error?.message||'');return value||response;
}
try {
 await client.connect(transport);
 save('server-version',client.getServerVersion());
 const catalog=await client.listTools();
 save('capability-names',catalog.tools.map(t=>t.name));
 save('target-identity',{name,mode,path:target,sha256:crypto.createHash('sha256').update(fs.readFileSync(target)).digest('hex')});
 if(mode==='followup') {
  for(const r of JSON.parse(fs.readFileSync(process.argv[4],'utf8')))await call(r.label,r.tool,r.arguments);
 } else if(mode==='native') {
  await call('open','open_binary',{path:target,provider_id:'ghidra'});
  const overview=await call('overview','binary_overview');
  if(overview.status==='error'||overview.error) {await call('session','binary_session');}
  else {
   await call('procedures','list_procedures');
   await call('strings','list_strings');
   await call('marker-search','search_strings',{pattern:'LICENSE_KEY_CHECK_V1'});
   await call('function-search','search_procedures',{pattern:'secret_transform'});
   for(const procedure of ['secret_transform','simple_checksum','main']) {
    for(const [suffix,tool] of [['info','procedure_info'],['pseudocode','procedure_pseudo_code'],['assembly','procedure_assembly'],['instructions','read_function_instructions'],['callees','procedure_callees'],['callers','procedure_callers'],['references','procedure_references'],['dossier','analyze_function']])
     await call(procedure+'-'+suffix,tool,{procedure});
   }
   await call('session','binary_session');
  }
  await call('close','close_binary');
 } else if(mode==='python') {
  await call('open','open_binary',{path:target,provider_id:'ghidra'});
  await call('session','binary_session');
  await call('overview','binary_overview');
  await call('close','close_binary');
 } else if(mode==='managed') {
  await call('artifact','inspect_managed_artifact',{path:target});
  await call('members','inspect_managed_members',{path:target});
  await call('native-boundaries','inspect_managed_native_boundaries',{path:target});
 } else if(mode==='js') {
  await call('single-file-analysis','analyze_javascript_application',{input_path:target});
  await call('application','analyze_javascript_application',{input_path:path.join(root,'docs/probe/samples/bin/target_js_app'),format:'directory'});
 }
} finally {await client.close();}
