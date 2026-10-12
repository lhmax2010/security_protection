TARGET_PATH="/home/linhao/Toolchain/development/security_optimization_rea/docs/probe/samples/bin/target_c_llvm_armv7l"
TARGET_KIND="executable"
-- Read-only ELF metadata decoder for RPM's already installed Lua 5.1 interpreter.
-- No target execution, file writes, native code bytes or rodata are emitted.
-- Caller supplies TARGET_PATH and TARGET_KIND; output is explicitly not readelf.
local f=assert(io.open(TARGET_PATH,"rb"))
local filesize=assert(f:seek("end"))
local function read(off,n)
 assert(off>=0 and n>=0 and off+n<=filesize,"metadata range exceeds file")
 assert(f:seek("set",off))
 local s=f:read(n); assert(s and #s==n,"short metadata read"); return s
end
local ident=read(0,16)
assert(ident:sub(1,4)=="\127ELF","not an ELF file")
local class=ident:byte(5);local encoding=ident:byte(6)
assert(class==1 or class==2,"unsupported ELF class")
assert(encoding==1 or encoding==2,"unsupported ELF encoding")
local function uint(off,n)
 local s=read(off,n);local result=0
 if encoding==1 then for i=n,1,-1 do result=result*256+s:byte(i) end
 else for i=1,n do result=result*256+s:byte(i) end end
 assert(result<=9007199254740991,"64-bit field exceeds exact Lua integer range")
 return result
end
local function hex(v)
 if v==0 then return "0x0" end
 local chars="0123456789abcdef";local s=""
 while v>0 do local q=math.floor(v/16);local digit=v-q*16;s=chars:sub(digit+1,digit+1)..s;v=q end
 return "0x"..s
end
local function emit(...)
 local a={...};for i=1,#a do a[i]=tostring(a[i]) end;io.write(table.concat(a,"\t"),"\n")
end
local function bit(v,mask) return math.floor(v/mask)-math.floor(v/(mask*2))*2==1 end
local function cstr(off,limit)
 assert(limit>0,"string offset outside table")
 local n=math.min(limit,4096);local s=read(off,n);local ending=s:find("\0",1,true)
 assert(ending,"metadata string not terminated within 4096-byte limit")
 local text=s:sub(1,ending-1)
 assert(not text:find("[\r\n\t]"),"metadata string contains control separators")
 return text
end
local word=class==1 and 4 or 8
local elf_type=uint(16,2);local machine=uint(18,2)
local phoff=uint(class==1 and 28 or 32,word)
local shoff=uint(class==1 and 32 or 40,word)
local phent=uint(class==1 and 42 or 54,2)
local phnum=uint(class==1 and 44 or 56,2)
local shent=uint(class==1 and 46 or 58,2)
local shnum=uint(class==1 and 48 or 60,2)
local shstr=uint(class==1 and 50 or 62,2)
local function section(i)
 local o=shoff+i*shent
 if class==1 then return {index=i,nameidx=uint(o,4),type=uint(o+4,4),flags=uint(o+8,4),addr=uint(o+12,4),offset=uint(o+16,4),size=uint(o+20,4),link=uint(o+24,4),info=uint(o+28,4),entsize=uint(o+36,4)} end
 return {index=i,nameidx=uint(o,4),type=uint(o+4,4),flags=uint(o+8,8),addr=uint(o+16,8),offset=uint(o+24,8),size=uint(o+32,8),link=uint(o+40,4),info=uint(o+44,4),entsize=uint(o+56,8)}
end
if shoff>0 then
 local zero=section(0)
 if shnum==0 then shnum=zero.size end
 if shstr==65535 then shstr=zero.link end
 if phnum==65535 then phnum=zero.info end
end
assert(phnum<=4096 and shnum<=65536,"metadata count limit exceeded")
assert((phnum==0 or phent>=(class==1 and 32 or 56)) and (shnum==0 or shent>=(class==1 and 40 or 64)),"invalid entry sizes")
emit("METHOD","RPM_EMBEDDED_LUA_DIRECT_ELF_METADATA","Lua=".._VERSION)
emit("TARGET",TARGET_PATH,TARGET_KIND)
emit("HEADER","class",class==1 and "ELF32" or "ELF64","encoding",encoding==1 and "LSB" or "MSB","type",elf_type,"machine",machine,"phoff",hex(phoff),"phnum",phnum,"shoff",hex(shoff),"shnum",shnum)
local gnu_relro=false;local gnu_stack=nil;local interpreter=false
for i=0,phnum-1 do
 local o=phoff+i*phent;local t=uint(o,4)
 local offset=uint(o+(class==1 and 4 or 8),word)
 local vaddr=uint(o+(class==1 and 8 or 16),word)
 local filesz=uint(o+(class==1 and 16 or 32),word)
 local memsz=uint(o+(class==1 and 20 or 40),word)
 local flags=uint(o+(class==1 and 24 or 4),4)
 emit("PROGRAM_HEADER",i,hex(t),"offset",hex(offset),"vaddr",hex(vaddr),"filesz",filesz,"memsz",memsz,"flags",flags)
 if t==1685382482 then gnu_relro=true end
 if t==1685382481 then gnu_stack=flags end
 if t==3 then interpreter=true;emit("INTERPRETER",cstr(offset,filesz)) end
end
local sections={};local stripped=true
for i=0,shnum-1 do sections[i]=section(i) end
if shnum>0 then
 assert(shstr<shnum,"invalid shstr index");local names=sections[shstr]
 for i=0,shnum-1 do
  local s=sections[i];s.name=cstr(names.offset+s.nameidx,names.size-s.nameidx)
  emit("SECTION",i,s.name,s.type,"offset",hex(s.offset),"size",s.size,"link",s.link,"entsize",s.entsize)
  if s.name==".symtab" then stripped=false end
 end
end
local bindnow=false;local pieflag=false;local rpath=nil;local runpath=nil;local dynamic_present=false;local dynsym_present=false
local canary_import=false;local canary_definition=false;local fortify_import=false;local fortify_definition=false
local exports=0;local exports_noabs=0;local exported_functions=0
for i=0,shnum-1 do
 local s=sections[i]
 if s.type==6 then
  dynamic_present=true;local entsize=s.entsize;assert(entsize>=word*2,"invalid dynamic entry size")
  local str=assert(sections[s.link],"dynamic string table missing")
  for j=0,math.floor(s.size/entsize)-1 do
   local o=s.offset+j*entsize;local tag=uint(o,word);local value=uint(o+word,word)
   emit("DYNAMIC",hex(tag),hex(value))
   if tag==0 then break end
   if tag==24 or (tag==30 and bit(value,8)) or (tag==1879048187 and bit(value,1)) then bindnow=true end
   if tag==1879048187 and bit(value,134217728) then pieflag=true end
   if tag==15 then rpath=cstr(str.offset+value,str.size-value);emit("RPATH_VALUE",rpath) end
   if tag==29 then runpath=cstr(str.offset+value,str.size-value);emit("RUNPATH_VALUE",runpath) end
  end
 elseif s.type==11 then
  dynsym_present=true;local entsize=s.entsize;assert(entsize>=(class==1 and 16 or 24),"invalid dynsym entry size")
  local strings=assert(sections[s.link],"dynsym string table missing")
  for j=0,math.floor(s.size/entsize)-1 do
   local o=s.offset+j*entsize;local nameidx=uint(o,4)
   local info=uint(o+(class==1 and 12 or 4),1);local other=uint(o+(class==1 and 13 or 5),1)
   local ndx=uint(o+(class==1 and 14 or 6),2)
   local bind=math.floor(info/16);local kind=info-bind*16;local vis=other-math.floor(other/4)*4
   local name=cstr(strings.offset+nameidx,strings.size-nameidx)
   local value=uint(o+(class==1 and 4 or 8),word)
   emit("DYNAMIC_SYMBOL",j,hex(value),"type",kind,"bind",bind,"vis",vis,"ndx",ndx,"name",name)
   local plain=name:gsub("@.*","")
   local canary=plain=="__stack_chk_fail" or plain=="__stack_chk_fail_local" or plain=="__stack_chk_guard"
   local fortify=plain:match("^__[A-Za-z0-9_]+_chk$")~=nil
   if ndx==0 then canary_import=canary_import or canary;fortify_import=fortify_import or fortify
   else
    canary_definition=canary_definition or canary;fortify_definition=fortify_definition or fortify
    if (bind==1 or bind==2) and (vis==0 or vis==3) and name~="" then
     exports=exports+1;if ndx~=65521 then exports_noabs=exports_noabs+1 end
     if kind==2 or kind==10 then exported_functions=exported_functions+1 end
     emit("EXPORT",kind,bind,vis,ndx,name)
    end
   end
  end
 elseif s.name==".comment" and s.size<=16384 then
  local text=read(s.offset,s.size);for line in text:gmatch("[^\0]+") do emit("COMPILER_COMMENT",line) end
 end
end
local function indicator(imported,defined)
 if not dynsym_present then return "Unknown(no dynsym)" end
 if imported then return "Detected(import)" end
 if defined then return "Provider-definition-only" end
 return "No dynamic evidence"
end
local relro=gnu_relro and (bindnow and "Full" or "Partial") or "None"
local nx=gnu_stack==nil and "Unknown(no GNU_STACK)" or (bit(gnu_stack,1) and "Disabled" or "Enabled")
local pie="Unknown"
if TARGET_KIND=="shared-library" then pie="N/A(DSO)"
elseif elf_type==2 then pie="No"
elseif elf_type==3 and (interpreter or pieflag) then pie="Yes" end
emit("FIELD","RELRO",relro);emit("FIELD","NX",nx);emit("FIELD","PIE",pie)
emit("FIELD","canary",indicator(canary_import,canary_definition));emit("FIELD","FORTIFY",indicator(fortify_import,fortify_definition))
emit("FIELD","stripped",shnum==0 and "Unknown(no section table)" or (stripped and "Yes(no .symtab)" or "No"))
emit("FIELD","RPATH",rpath and "Present" or "Absent");emit("FIELD","RUNPATH",runpath and "Present" or "Absent")
emit("FIELD","dynamic_export_count_including_ABS",exports);emit("FIELD","dynamic_export_non_ABS_count",exports_noabs);emit("FIELD","dynamic_export_function_count",exported_functions)
f:close()
emit("METADATA_READER_SUCCESS")
