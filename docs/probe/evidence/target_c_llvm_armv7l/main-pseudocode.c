
undefined4 main(int param_1,int param_2)

{
  ulong uVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  
  uVar1 = 0x4d2;
  if (1 < param_1) {
    uVar1 = strtoul(*(char **)(param_2 + 4),(char **)0x0,10);
  }
  uVar2 = secret_transform(uVar1);
  uVar3 = simple_checksum("LICENSE_KEY_CHECK_V1");
  printf("%s %u %u\n","LICENSE_KEY_CHECK_V1",uVar2,uVar3);
  return 0;
}

