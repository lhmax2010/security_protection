import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
const root=process.env.PROBE_ROOT;
const {skillDestinations,readInstalledSkillIdentity}=await import(path.join(root,'.local-tools/rea/node_modules/rea-agents/dist/application/SetupSkill.js'));
const ids=JSON.parse(fs.readFileSync(path.join(root,'docs/probe/evidence/doctor-codex.json'))).identity.registrations.map(x=>x.client);
const inspect=async clients=>({clients,identity:await readInstalledSkillIdentity(os.homedir(),clients,process.env),destinations:skillDestinations(os.homedir(),clients,process.env).map(x=>({...x,skill_file_exists:fs.existsSync(path.join(x.path,'SKILL.md'))}))});
console.log(JSON.stringify({codex_scope:await inspect(['codex']),audit_scope:await inspect(ids)},null,2));
