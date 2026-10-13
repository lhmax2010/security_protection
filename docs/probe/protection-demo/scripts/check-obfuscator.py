#!/usr/bin/env python3
"""Bounded, read-only capability check; no obfuscator acquisition or builds."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess

base = Path('docs/probe/protection-demo')
args = [shutil.which('clang-18'), '-cc1', '-mllvm', '--help-hidden']
p = subprocess.run(args, capture_output=True, text=True)
runtime = base / 'local-runtime'
runtime.mkdir(exist_ok=True)
(runtime / 'clang-hidden-options.txt').write_text(p.stdout + p.stderr)
if p.returncode:
    (base / 'obfuscator-option-check-error.txt').write_text(p.stdout + p.stderr + f'\nexit={p.returncode}\n')
    raise SystemExit(p.returncode)
selectors = re.compile(r'^\s+--?(?:fla(?:-loop|-prob)?|bcf(?:-loop|-prob)?|sub(?:-loop|-prob)?|sobf|split(?:-num)?|enable-cffobf|enable-bcfobf|enable-subobf)(?:[ =]|$)')
matched = [line for line in p.stdout.splitlines() if selectors.search(line)]
commands = {name: shutil.which(name) for name in ['tigress', 'ollvm', 'clang-ollvm', 'clang-obfuscator', 'obfuscator-llvm', 'cobfuscator']}
candidates = []
for directory in dict.fromkeys(os.environ['PATH'].split(os.pathsep)):
    d = Path(directory)
    if d.is_dir():
        candidates += [str(f) for f in d.iterdir() if re.search(r'tigress|ollvm|obfus', f.name, re.I) and os.access(f, os.X_OK)]
available = bool(matched or any(commands.values()) or candidates)
record = {'command': args, 'exit': p.returncode, 'option_output_sha256': hashlib.sha256(p.stdout.encode()).hexdigest(),
    'option_lines': len(p.stdout.splitlines()), 'known_obfuscation_selectors': matched,
    'common_native_obfuscator_commands': commands, 'PATH_candidate_executables': candidates,
    'review_of_initial_matches': 'split-dwarf-cross-cu-references is DWO debugging; split-spill-mode and split-threshold-for-reg-with-hint concern register allocation, not obfuscation.',
    'ready_obfuscator_found': available,
    'decision': 'Inspect candidates before using' if available else 'No ready native C/ARM obfuscator found in bounded checks; code obfuscation is a next step, not performed this round.',
    'scope': 'PATH executable names, installed Clang18 LLVM option inventory, and earlier .local-tools file-name inventory; not a proof of absence from every machine directory.',
    'no_download_or_obfuscator_build_or_handmade_obfuscation': True}
(base / 'obfuscator-availability.json').write_text(json.dumps(record, indent=2) + '\n')
assert not available, 'Inspect candidates before deciding.'
print('No ready native obfuscator found in bounded checks; optional obfuscation not performed.')
