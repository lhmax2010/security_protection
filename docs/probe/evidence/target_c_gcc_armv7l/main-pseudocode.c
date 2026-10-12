
undefined4 main(int param_1,int param_2)

{
  ulong uVar1;
  undefined4 uVar2;
  undefined8 uVar3;
  
  if (param_1 < 2) {
    uVar1 = 0x4d2;
  }
  else {
    uVar1 = strtoul(*(char **)(param_2 + 4),(char **)0x0,10);
  }
  uVar2 = secret_transform(uVar1);
  uVar3 = simple_checksum("LICENSE_KEY_CHECK_V1","%s %u %u\n");
  __printf_chk(2,(int)((ulonglong)uVar3 >> 0x20),"LICENSE_KEY_CHECK_V1",uVar2,(int)uVar3);
  return 0;
}

