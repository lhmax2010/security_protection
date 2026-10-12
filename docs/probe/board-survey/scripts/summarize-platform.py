#!/usr/bin/env python3
from pathlib import Path
import re,json
r=Path(__file__).resolve().parents[1];s=(r/'platform-mechanisms.txt').read_text()
value=re.search(r'COMMAND: cat /proc/sys/kernel/randomize_va_space\n(\d+)\n\nEXIT_CODE: 0',s);assert value
root=re.search(r'(?m)^(/dev/\S+) / (\S+) ([^\n]+)',s);assert root
mounts=[l for l in s.splitlines() if ' on ' in l and ' type ' in l]
smack=next((l for l in mounts if ' on /sys/fs/smackfs type smackfs ' in l),None)
report={'smackfs_directory_observed':True,'smackfs_mounted':smack is not None,'smack_mount':smack,'smack_rule_contents_dumped':False,'ASLR_randomize_va_space':int(value[1]),'root_device':root[1],'root_filesystem':root[2],'root_mount_options':root[3].split(' ')[0].split(','),'root_readonly':'ro' in root[3].split(' ')[0].split(','),'opt_writable_observed':any(' on /opt type ' in l and '(rw,' in l for l in mounts),'verity_keyword_observed_in_mounts':any('verity' in l.lower() for l in mounts),'dm_block_sysfs_directory_observed':'DM_DEVICE_DIRECTORY_OBSERVED: yes' in s,'lsm_listing_unavailable':'cat: /sys/kernel/security/lsm: No such file or directory' in s,'limits':['SMACK presence/mount/context observed; rules/enforcement exceptions not audited.','ASLR kernel setting observed; no runtime address sampling.','No dm/verity trace in this bounded mount/sysfs query does not establish absence of all firmware integrity or verified boot.','Read-only root and writable /opt are compatible with persisting ConnMan settings in /opt.']}
(r/'platform-mechanisms-summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
