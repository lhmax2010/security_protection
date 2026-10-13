#!/usr/bin/env python3
"""Run with docs/probe/scripts/env.sh sourced; never rebuild the baseline."""
from pathlib import Path
import hashlib
import json
import shlex
import subprocess

root = Path.cwd()
demo = root / 'docs/probe/protection-demo'
tools = root / '.local-tools/sysroot/usr'
binary = demo / 'bin/target_c_llvm_armv7l_protected'
baseline = root / 'docs/probe/samples/bin/target_c_llvm_armv7l'
binary.parent.mkdir(exist_ok=True)
commands = []

def run(args, output=None):
    commands.append(shlex.join(map(str, args)))
    (demo / 'build-flags.txt').write_text('\n'.join(commands) + '\n')
    p = subprocess.run(list(map(str, args)), capture_output=True, text=True)
    if output:
        (demo / output).write_text('$ ' + commands[-1] + '\n' + p.stdout + p.stderr + f'\nexit={p.returncode}\n')
    if p.returncode:
        raise RuntimeError(p.stdout + p.stderr + f'\nexit={p.returncode}')
    return p.stdout

run([tools / 'bin/clang-18', '--version'], 'compiler-version.txt')
run([tools / 'bin/clang-18', '--target=arm-linux-gnueabihf',
     '--sysroot=' + str(tools.parent), '--gcc-toolchain=' + str(tools),
     '-isystem', tools / 'arm-linux-gnueabihf/include',
     '-L' + str(tools / 'arm-linux-gnueabihf/lib'),
     '-march=armv7-a', '-mfpu=vfpv3-d16',
     '-fvisibility=hidden', '-fvisibility-inlines-hidden',
     '-fstack-protector-strong', '-D_FORTIFY_SOURCE=2', '-O2',
     '-fPIE', '-Wl,-z,relro', '-Wl,-z,now', '-pie',
     demo / 'src/target_protected.c', '-o', binary], 'build-log.txt')
run([tools / 'bin/arm-linux-gnueabihf-readelf', '-Ws', binary], 'pre-strip-symbols.txt')
symbols = (demo / 'pre-strip-symbols.txt').read_text().splitlines()
addresses = {}
for line in symbols:
    fields = line.split()
    if len(fields) == 8 and fields[-1] in ('secret_transform', 'simple_checksum', 'main'):
        addresses[fields[-1]] = {'elf_value': fields[1], 'size': int(fields[2]),
                               'binding': fields[4], 'visibility': fields[5]}
assert len(addresses) == 3, addresses
(demo / 'function-addresses.json').write_text(json.dumps({
    'method': 'Compiler-assisted ground truth from pre-strip readelf, not a blind REA discovery',
    'functions': addresses}, indent=2) + '\n')
run([tools / 'bin/arm-linux-gnueabihf-strip', '--strip-all', binary], 'strip-log.txt')
run(['file', binary], 'file.txt')
cases = [[], ['0'], ['1'], ['1234'], ['65535'], ['65536'], ['4294967295'],
         ['4294967296'], ['-1'], ['not-a-number'], ['42', 'extra']]
qemu = [str(tools / 'bin/qemu-arm'), '-L', str(tools / 'arm-linux-gnueabihf')]
records = []
for args in cases:
    pair = []
    for target in [baseline, binary]:
        cmd = qemu + [str(target)] + args
        p = subprocess.run(cmd, capture_output=True, timeout=20)
        pair.append({'command': shlex.join(cmd), 'exit': p.returncode,
                     'stdout': p.stdout.decode(), 'stderr': p.stderr.decode()})
    equal = pair[0]['exit'] == pair[1]['exit'] == 0 and pair[0]['stdout'] == pair[1]['stdout'] and pair[0]['stderr'] == pair[1]['stderr'] == ''
    records.append({'args': args, 'baseline': pair[0], 'protected': pair[1], 'equal': equal})
    (demo / 'run-equivalence.json').write_text(json.dumps(records, indent=2) + '\n')
    assert equal, records[-1]
(demo / 'run-equivalence.txt').write_text(
    'QEMU ARM user-mode; existing baseline reused without rebuild.\n'
    'Equality: exit=0, identical stdout, empty stderr in both runs.\n' +
    '\n'.join(f'args={r["args"]!r}: MATCH {r["protected"]["stdout"].strip()}' for r in records) +
    '\nCoverage: 11 cases including defaults, boundaries, invalid/overflow input, extra args; not exhaustive equivalence proof.\n')
manifest = {str(p.relative_to(root)): {'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size}
            for p in [baseline, binary, demo / 'src/target_protected.c']}
(demo / 'artifact-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
assert b'LICENSE_KEY_CHECK_V1' not in binary.read_bytes(), 'plaintext in final binary'
print(f'Built and fully stripped {binary.stat().st_size} bytes; QEMU equivalence 11/11; no marker bytes in binary.')
