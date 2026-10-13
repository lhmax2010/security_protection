import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const root=process.env.PROBE_ROOT;
const base=path.join(root,'docs/probe/protection-demo/obfuscation');
const {Client}=await import(path.join(root,'.local-tools/rea/node_modules/@modelcontextprotocol/client/dist/index.mjs'));
const {StdioClientTransport}=await import(path.join(root,'.local-tools/rea/node_modules/@modelcontextprotocol/client/dist/stdio.mjs'));
const client=new Client({name:'obfuscation-demo',version:'1.0.0'});
const transport=new StdioClientTransport({command:path.join(root,'.local-tools/node-v24.21.0-linux-x64/bin/node'),
  args:[path.join(root,'.local-tools/rea/node_modules/rea-agents/scripts/rea.mjs'),'mcp'],env:{...process.env},stderr:'pipe'});
let dir,records,opened=false;
transport.stderr?.on('data',d=>{if(dir)fs.appendFileSync(path.join(dir,'mcp-stderr.txt'),d);});
const save=(label,value)=>fs.writeFileSync(path.join(dir,label+'.json'),JSON.stringify(value,null,2)+'\n');
async function call(label,tool,args={}) {
  const start=Date.now();let response;
  try{response=await client.callTool({name:tool,arguments:args},undefined,{timeout:600000});}
  catch(e){response={transport_error:{name:e.name,message:e.message,code:e.code,data:e.data}};}
  save(label,response);let value=response.structuredContent;
  if(!value)for(const c of response.content||[])if(c.type==='text'){try{value=JSON.parse(c.text);break;}catch{}}
  if(value)save(label+'.decoded',value);
  records.push({label,tool,arguments:args,elapsed_ms:Date.now()-start,isError:!!response.isError,transport_error:response.transport_error||null});
  save('requests',records);console.log(path.basename(dir),label,Date.now()-start+'ms');
  if(response.isError||response.transport_error||value?.status==='error'||value?.error)throw new Error(JSON.stringify(response));
  return value;
}
try {
  await client.connect(transport);
  for(const [folder,binary] of [['control22','target_c_llvm22_control'],['obfuscated','target_c_llvm22_obfuscated']]) {
    dir=path.join(base,folder);fs.mkdirSync(dir,{recursive:true});records=[];
    const target=path.join(base,'bin',binary);
    save('server-version',client.getServerVersion());
    save('target-identity',{path:target,sha256:crypto.createHash('sha256').update(fs.readFileSync(target)).digest('hex')});
    await call('open','open_binary',{path:target,provider_id:'ghidra'});opened=true;
    await call('overview','binary_overview');
    for(const procedure of ['secret_transform','simple_checksum']) {
      await call(procedure+'-search','search_procedures',{pattern:procedure});
      await call(procedure+'-info','procedure_info',{procedure});
      const pseudo=await call(procedure+'-pseudocode','procedure_pseudo_code',{procedure});
      fs.writeFileSync(path.join(dir,procedure+'-pseudocode.c'),pseudo.normalized_result);
      await call(procedure+'-assembly','procedure_assembly',{procedure});
      await call(procedure+'-instructions','read_function_instructions',{procedure});
    }
    await call('close','close_binary');opened=false;
  }
} finally {
  if(opened)await call('close','close_binary');
  await client.close();
}
