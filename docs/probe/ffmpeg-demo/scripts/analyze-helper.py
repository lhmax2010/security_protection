#!/usr/bin/env python3
import os,sys,json,subprocess
from pathlib import Path
variant,target=sys.argv[1:]
r=Path(__file__).resolve().parents[1]
callees=json.loads((r/'private/rea'/variant/'av_get_audio_frame_duration2/callees.decoded.json').read_text())['normalized_result']
assert len(callees)==1, 'Select helper manually if multiple callees'
env=os.environ.copy();env.update(REA_RUN_LABEL=variant+'-helper',REA_FOLLOWUP_ADDRESS=callees[0])
with (r/'private'/('rea-'+variant+'-helper-progress.txt')).open('w') as f:
 subprocess.run(['node',str(r/'scripts/analyze.mjs'),variant,target],env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
