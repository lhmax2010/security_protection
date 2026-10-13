
void FUN_00010624(int param_1,int param_2)

{
  undefined4 uVar1;
  undefined4 uVar2;
  ulong uVar3;
  undefined1 local_29;
  undefined1 local_28;
  undefined1 local_27;
  undefined1 local_26;
  undefined1 local_25;
  undefined1 local_24;
  undefined1 local_23;
  undefined1 local_22;
  undefined1 local_21;
  undefined1 local_20;
  undefined1 local_1f;
  undefined1 local_1e;
  undefined1 local_1d;
  undefined1 local_1c;
  undefined1 local_1b;
  undefined1 local_1a;
  undefined1 local_19;
  undefined1 local_18;
  undefined1 local_17;
  undefined1 local_16;
  undefined1 local_15;
  int local_14;
  
  local_14 = __stack_chk_guard;
  local_29 = 0x4c;
  local_28 = 0x49;
  local_27 = 0x43;
  local_26 = 0x45;
  local_25 = 0x4e;
  local_24 = 0x53;
  local_23 = 0x45;
  local_22 = 0x5f;
  local_21 = 0x4b;
  local_20 = 0x45;
  local_1f = 0x59;
  local_1e = 0x5f;
  local_1d = 0x43;
  local_1c = 0x48;
  local_1b = 0x45;
  local_1a = 0x43;
  local_19 = 0x4b;
  local_18 = 0x5f;
  local_17 = 0x56;
  local_16 = 0x31;
  uVar3 = 0x4d2;
  local_15 = 0;
  if (1 < param_1) {
    uVar3 = strtoul(*(char **)(param_2 + 4),(char **)0x0,10);
  }
  uVar1 = FUN_000105d0(uVar3);
  uVar2 = FUN_000105e8(&local_29);
  __printf_chk(1,"%s %u %u\n",&local_29,uVar1,uVar2);
  if (__stack_chk_guard != local_14) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail(local_14);
  }
  return;
}

