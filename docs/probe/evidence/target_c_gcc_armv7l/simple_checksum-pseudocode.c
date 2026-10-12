
short simple_checksum(byte *param_1)

{
  short sVar1;
  ushort uVar2;
  
  uVar2 = (ushort)*param_1;
  if (uVar2 != 0) {
    sVar1 = 0;
    do {
      sVar1 = sVar1 * 0x1f + uVar2;
      param_1 = param_1 + 1;
      uVar2 = (ushort)*param_1;
    } while (uVar2 != 0);
    return sVar1;
  }
  return 0;
}

