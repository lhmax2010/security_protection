#!/usr/bin/env python3
# Host-only validation using an existing Lua shared library; no installation.
import ctypes,ctypes.util,sys
from pathlib import Path
lib=ctypes.CDLL(ctypes.util.find_library('lua5.3'))
lib.luaL_newstate.restype=ctypes.c_void_p;lib.luaL_openlibs.argtypes=[ctypes.c_void_p]
lib.luaL_loadbufferx.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_size_t,ctypes.c_char_p,ctypes.c_char_p];lib.luaL_loadbufferx.restype=ctypes.c_int
lib.lua_pcallk.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_ssize_t,ctypes.c_void_p];lib.lua_pcallk.restype=ctypes.c_int
lib.lua_tolstring.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.POINTER(ctypes.c_size_t)];lib.lua_tolstring.restype=ctypes.c_char_p
lib.lua_close.argtypes=[ctypes.c_void_p]
code=Path(sys.argv[1]).read_bytes();state=lib.luaL_newstate();lib.luaL_openlibs(state)
result=lib.luaL_loadbufferx(state,code,len(code),b'survey-validation',None)
if result==0:result=lib.lua_pcallk(state,0,0,0,0,None)
if result:print(lib.lua_tolstring(state,-1,None).decode(),file=sys.stderr)
lib.lua_close(state);raise SystemExit(bool(result))
