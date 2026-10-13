#!/usr/bin/env python3
"""Reuse the validated read-only Lua decoder; cross-check real GNU readelf."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

root = Path.cwd()
demo = root / 'docs/probe/protection-demo'
survey = root / 'docs/probe/board-survey/scripts'
out = demo / 'elf'
runtime = demo / 'local-runtime'
out.mkdir(exist_ok=True)
runtime.mkdir(exist_ok=True)
decoder = survey / 'elf-metadata.lua'
summary = {'method': 'Existing validated elf-metadata.lua via host Lua 5.3 ctypes runner; independent GNU readelf cross-check. No REA attribution.',
           'decoder_sha256': hashlib.sha256(decoder.read_bytes()).hexdigest(), 'targets': {}}
targets = {'baseline': root / 'docs/probe/samples/bin/target_c_llvm_armv7l',
           'protected': demo / 'bin/target_c_llvm_armv7l_protected'}
for name, target in targets.items():
    lua = runtime / (name + '.lua')
    lua.write_text('TARGET_PATH=' + json.dumps(str(target)) + '\nTARGET_KIND="executable"\n' + decoder.read_text())
    args = ['python3', str(survey / 'lua-host-run.py'), str(lua)]
    p = subprocess.run(args, capture_output=True, text=True)
    (out / (name + '-lua.txt')).write_text(p.stdout + p.stderr + f'\nexit={p.returncode}\n')
    assert p.returncode == 0 and 'METADATA_READER_SUCCESS' in p.stdout, p.stderr
    fields = {line.split('\t')[1]: line.split('\t')[2] for line in p.stdout.splitlines() if line.startswith('FIELD\t')}
    ref = subprocess.run(['readelf', '-W', '-h', '-l', '-S', '-d', '--dyn-syms', str(target)], capture_output=True, text=True)
    (out / (name + '-readelf.txt')).write_text(ref.stdout + ref.stderr + f'\nexit={ref.returncode}\n')
    assert ref.returncode == 0, ref.stderr
    text = ref.stdout
    expected = {'RELRO': 'None' if 'GNU_RELRO' not in text else ('Full' if re.search(r'\(BIND_NOW\)|\(FLAGS(?:_1)?\).*\bNOW\b', text) else 'Partial')}
    stack = next(line for line in text.splitlines() if re.match(r'^\s*GNU_STACK\s', line))
    expected['NX'] = 'Disabled' if 'E' in ''.join(stack.split()[6:-1]) else 'Enabled'
    expected['PIE'] = 'Yes' if re.search(r'\bDYN\b', text) and ('INTERP' in text or re.search(r'\(FLAGS_1\).*\bPIE\b', text)) else 'No'
    expected['stripped'] = 'No' if re.search(r'(?m)^\s*\[\s*\d+\]\s+\.symtab\s', text) else 'Yes(no .symtab)'
    expected['RPATH'] = 'Present' if '(RPATH)' in text else 'Absent'
    expected['RUNPATH'] = 'Present' if '(RUNPATH)' in text else 'Absent'
    symbols = []
    for line in text.splitlines():
        m = re.match(r'^\s*\d+:\s+([0-9a-fA-F]+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)', line)
        if m:
            symbols.append(dict(zip(['value', 'size', 'type', 'bind', 'vis', 'ndx', 'name'], m.groups())))
    for key, predicate in [('canary', lambda n: n.split('@')[0] in ['__stack_chk_fail', '__stack_chk_fail_local', '__stack_chk_guard']),
                           ('FORTIFY', lambda n: bool(re.fullmatch(r'__[A-Za-z0-9_]+_chk', n.split('@')[0])))]:
        expected[key] = 'Detected(import)' if any(s['ndx'] == 'UND' and predicate(s['name']) for s in symbols) else ('Provider-definition-only' if any(s['ndx'] != 'UND' and predicate(s['name']) for s in symbols) else 'No dynamic evidence')
    exports = [s for s in symbols if s['ndx'] != 'UND' and s['bind'] in ['GLOBAL', 'WEAK'] and s['vis'] in ['DEFAULT', 'PROTECTED']]
    expected['dynamic_export_count_including_ABS'] = str(len(exports))
    expected['dynamic_export_non_ABS_count'] = str(sum(s['ndx'] != 'ABS' for s in exports))
    expected['dynamic_export_function_count'] = str(sum(s['type'] in ['FUNC', 'IFUNC'] for s in exports))
    mismatches = {k: {'lua': fields.get(k), 'readelf': v} for k, v in expected.items() if fields.get(k) != v}
    full = subprocess.run(['readelf', '-Ws', str(target)], capture_output=True, text=True)
    (out / (name + '-all-symbols.txt')).write_text(full.stdout + full.stderr + f'\nexit={full.returncode}\n')
    assert full.returncode == 0, full.stderr
    marker = b'LICENSE_KEY_CHECK_V1'
    strp = subprocess.run(['strings', '-a', str(target)], capture_output=True, text=True)
    (out / (name + '-strings.txt')).write_text(strp.stdout + strp.stderr + f'\nexit={strp.returncode}\n')
    assert strp.returncode == 0, strp.stderr
    summary['targets'][name] = {'path': str(target.relative_to(root)), 'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
        'fields': fields, 'expected_from_GNU_readelf': expected, 'mismatches': mismatches,
        'marker_bytes_found': marker in target.read_bytes(),
        'marker_strings_hits': sum(marker.decode() in line for line in strp.stdout.splitlines()),
        'helper_symbol_rows': [line.strip() for line in full.stdout.splitlines() if line.split() and line.split()[-1] in ['secret_transform', 'simple_checksum', 'main']]}
    (demo / 'hardening-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    assert not mismatches, mismatches
print('Lua/GNU readelf agree for both ELFs:', {k: v['fields'] for k, v in summary['targets'].items()})
