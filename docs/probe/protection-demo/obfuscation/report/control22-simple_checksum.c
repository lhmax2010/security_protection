
short simple_checksum(byte *param_1)

{
  short sVar1;
  ushort uVar2;
  
  if (*param_1 != 0) {
    sVar1 = 0;
    uVar2 = (ushort)*param_1;
    do {
      param_1 = param_1 + 1;
      sVar1 = sVar1 * 0x1f + uVar2;
      uVar2 = (ushort)*param_1;
    } while (*param_1 != 0);
    return sVar1;
  }
  return 0;
}

