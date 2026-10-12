import pathlib,os
root=pathlib.Path('.local-tools/sysroot').resolve()
for p in (root/'usr/lib/jvm/java-21-openjdk-amd64/conf').rglob('*'):
 if p.is_symlink():
  target=os.readlink(p)
  if target.startswith('/etc/java-21-openjdk/'):
   local=root/target.lstrip('/')
   if not local.is_file(): raise RuntimeError(f'Missing packaged config: {local}')
   p.unlink();p.symlink_to(os.path.relpath(local,p.parent))
   print(p,'->',os.readlink(p))
