#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import subprocess

root = Path.cwd()
out = root / 'docs/probe/protection-demo/obfuscation'
local = root / '.local-tools/obfuscation'
asset = json.loads((out / 'selected-asset.json').read_text())['asset']
archive = local / asset['name']
toolchain = local / 'xollvm-v0.11.1'
local.mkdir(exist_ok=True)
expected = asset['digest'].split(':', 1)[1]
commands = []
def run(args, logfile):
    commands.append(list(map(str, args)))
    (out / 'acquisition-commands.json').write_text(json.dumps(commands, indent=2) + '\n')
    p = subprocess.run(list(map(str, args)), capture_output=True, text=True)
    (out / logfile).write_text(p.stdout + p.stderr + f'\nexit={p.returncode}\n')
    if p.returncode:
        raise RuntimeError(p.stdout + p.stderr + f'\nexit={p.returncode}')
    return p.stdout

if not archive.exists() or hashlib.sha256(archive.read_bytes()).hexdigest() != expected:
    run(['curl', '-fL', '--silent', '--show-error', '--connect-timeout', '30',
         '--max-time', '600', asset['browser_download_url'], '-o', archive], 'download-log.txt')
actual = hashlib.sha256(archive.read_bytes()).hexdigest()
assert actual == expected and archive.stat().st_size == asset['size'], 'Release digest/size mismatch'
toolchain.mkdir(exist_ok=True)
listing = subprocess.check_output(['tar', '--zstd', '-tf', str(archive)], text=True)
(local / 'archive-members.txt').write_text(listing)
assert all(not Path(p).is_absolute() and '..' not in Path(p).parts for p in listing.splitlines())
if not list(toolchain.rglob('clang')):
    run(['tar', '--zstd', '-xf', archive, '-C', toolchain], 'extraction-log.txt')
clang = next(p for p in toolchain.rglob('clang') if p.parent.name == 'bin')
opt = clang.with_name('opt')
version = run([clang, '--version'], 'clang-version.txt')
run([clang, '--print-targets'], 'clang-targets.txt')
run([opt, '--version'], 'opt-version.txt')
run([opt, '--print-passes'], 'opt-passes.txt')
record = {'repository': 'https://github.com/und3ath/xollvm', 'tag': 'v0.11.1',
          'commit': 'eb0850bd7cc87f551ad2948826605e518f5b8aa2', 'acquisition': 'upstream prebuilt, not locally built',
          'archive_sha256': actual, 'archive_bytes': archive.stat().st_size,
          'clang': str(clang), 'opt': str(opt), 'clang_version': version,
          'release_asset_digest_verified': True}
(out / 'toolchain.json').write_text(json.dumps(record, indent=2) + '\n')
(out / 'toolchain.txt').write_text('\n'.join(f'{k}: {v}' for k, v in record.items()) + '\n')
print(version.strip())
print('Verified release archive digest and size; toolchain path:', clang)
