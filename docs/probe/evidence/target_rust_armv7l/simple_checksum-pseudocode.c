
short simple_checksum(byte *param_1,int param_2)

{
  short sVar1;
  
  sVar1 = 0;
  for (; param_2 != 0; param_2 = param_2 + -1) {
    sVar1 = sVar1 * 0x1f + (ushort)*param_1;
    param_1 = param_1 + 1;
  }
  return sVar1;
}

