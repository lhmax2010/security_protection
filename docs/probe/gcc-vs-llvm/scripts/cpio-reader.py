"""newc regular file iterator, with hardlink contents; no filesystem extraction."""
def regular_files(data):
 pos=0;entries=[];content_by_inode={}
 while pos<len(data):
  head=data[pos:pos+110];assert head[:6] in [b'070701',b'070702'],(pos,head[:6])
  fields=[int(head[6+i*8:14+i*8],16) for i in range(13)]
  ino,mode,uid,gid,nlink,mtime,size,devmaj,devmin,rdevmaj,rdevmin,namesize,check=fields
  name=data[pos+110:pos+110+namesize-1].decode();pos=(pos+110+namesize+3)&~3
  content=data[pos:pos+size];assert len(content)==size;pos=(pos+size+3)&~3
  if name=='TRAILER!!!':break
  if mode&0o170000!=0o100000:continue
  key=(ino,devmaj,devmin)
  if size:content_by_inode[key]=content
  entries.append((name,content,key))
 for name,content,key in entries:yield name,content or content_by_inode.get(key,b'')
