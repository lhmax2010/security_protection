#!/usr/bin/env python3
"""Use the acquired LLVM22 compiler; fail on command/runtime errors, preserving logs."""
from pathlib import Path
import hashlib
import json
import shlex
import subprocess

root = Path.cwd()
base = root / 'docs/probe/protection-demo/obfuscation'
tools = root / '.local-tools/sysroot/usr'
clang = Path(json.loads((base / 'toolchain.json').read_text())['clang'])
for d in ['src', 'bin', 'build', 'pass-report', 'local-runtime']:
    (base / d).mkdir(exist_ok=True)
(base / '.gitignore').write_text('local-runtime/\n__pycache__/\n')
original = root / 'docs/probe/samples/target.c'
annotation = 'obf: substitution(prob=100,loop=2), bcf(prob=100,loop=1,maxBlocks=200), flattening(minBlocks=2,maxBlocks=200)'
source = original.read_text().replace('__attribute__((noinline,used))', '__attribute__((noinline,used,annotate("' + annotation + '")))')
annotated = base / 'src/target_obfuscated.c'
annotated.write_text(source)
commands = []
def run(args, label):
    cmd = list(map(str, args))
    commands.append({'label': label, 'command': cmd})
    (base / 'obf-build-commands.json').write_text(json.dumps(commands, indent=2) + '\n')
    (base / 'obf-build-flags.txt').write_text('Per-function annotation: ' + annotation + '\n' +
        '\n'.join(r['label'] + ': ' + shlex.join(r['command']) for r in commands) + '\n')
    p = subprocess.run(cmd, capture_output=True, text=True)
    (base / 'build' / (label + '.txt')).write_text('$ ' + shlex.join(cmd) + '\n' + p.stdout + p.stderr + f'\nexit={p.returncode}\n')
    if p.returncode:
        raise RuntimeError(p.stdout + p.stderr + f'\nexit={p.returncode}')
    return p.stdout

common = [clang, '--target=arm-linux-gnueabihf', '--sysroot=' + str(tools.parent),
          '--gcc-toolchain=' + str(tools), '-isystem', tools / 'arm-linux-gnueabihf/include',
          '-L' + str(tools / 'arm-linux-gnueabihf/lib'), '-O2', '-march=armv7-a', '-mfpu=vfpv3-d16']
obfflags = ['-mllvm', '-enable-obfuscation', '-mllvm', '-obf-seed=1', '-mllvm', '-obf-deterministic', '-mllvm', '-obf-verify']
plain = base / 'bin/target_c_llvm22_control'
obfuscated = base / 'bin/target_c_llvm22_obfuscated'
run(common + [original, '-o', plain], 'llvm22-control')
run(common + obfflags + ['-mllvm', '-obf-report-json=' + str(base / 'pass-report.json'),
    '-mllvm', '-obf-report-dir=' + str(base / 'pass-report'), annotated, '-o', obfuscated], 'llvm22-obfuscated')
run(['file', plain, obfuscated], 'elf-file')
run(['readelf', '-Ws', obfuscated], 'obfuscated-symbols')
cases = [[], ['0'], ['1'], ['1234'], ['65535'], ['65536'], ['4294967295'], ['4294967296'], ['-1'], ['not-a-number'], ['42', 'extra']]
qemu = [str(tools / 'bin/qemu-arm'), '-L', str(tools / 'arm-linux-gnueabihf')]
baseline = root / 'docs/probe/samples/bin/target_c_llvm_armv7l'
records = []
for args in cases:
    outputs = {}
    for name, target in [('baseline18', baseline), ('control22', plain), ('obfuscated22', obfuscated)]:
        cmd = qemu + [str(target)] + args
        p = subprocess.run(cmd, capture_output=True, timeout=30)
        outputs[name] = {'command': shlex.join(cmd), 'exit': p.returncode, 'stdout': p.stdout.decode(), 'stderr': p.stderr.decode()}
    equal = all(v['exit'] == 0 and v['stderr'] == '' and v['stdout'] == outputs['baseline18']['stdout'] for v in outputs.values())
    records.append({'args': args, 'outputs': outputs, 'equal': equal})
    (base / 'obf-run-equivalence.json').write_text(json.dumps(records, indent=2) + '\n')
    assert equal, records[-1]
(base / 'obf-run-equivalence.txt').write_text('Existing Clang18 baseline, Clang22 no-pass control, Clang22 annotated obfuscation: stdout/exit equal and stderr empty.\n' +
    '\n'.join(f'args={r["args"]!r}: MATCH {r["outputs"]["obfuscated22"]["stdout"].strip()}' for r in records) + '\n')
manifest = {str(p.relative_to(root)): {'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size}
            for p in [original, annotated, baseline, plain, obfuscated]}
(base / 'artifact-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print('Built LLVM22 control and annotated obfuscated ARM binaries; QEMU 11/11 matches across all three.')
