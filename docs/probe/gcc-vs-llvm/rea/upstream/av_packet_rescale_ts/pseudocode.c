
void av_packet_rescale_ts
               (int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
               undefined4 param_5)

{
  int iVar1;
  undefined8 uVar2;
  
  iVar1 = __stack_chk_guard;
  if (*(int *)(param_1 + 0xc) != -0x80000000 || *(int *)(param_1 + 8) != 0) {
    uVar2 = av_rescale_q(*(int *)(param_1 + 8),*(int *)(param_1 + 0xc),param_2,param_3,param_4,
                         param_5);
    *(undefined8 *)(param_1 + 8) = uVar2;
  }
  if (*(int *)(param_1 + 0x14) != -0x80000000 || *(int *)(param_1 + 0x10) != 0) {
    uVar2 = av_rescale_q(*(int *)(param_1 + 0x10),*(int *)(param_1 + 0x14),param_2,param_3,param_4,
                         param_5);
    *(undefined8 *)(param_1 + 0x10) = uVar2;
  }
  if ((int)(uint)(*(int *)(param_1 + 0x30) == 0) <= *(int *)(param_1 + 0x34)) {
    uVar2 = av_rescale_q(*(int *)(param_1 + 0x30),*(int *)(param_1 + 0x34),param_2,param_3,param_4,
                         param_5);
    *(undefined8 *)(param_1 + 0x30) = uVar2;
  }
  if (__stack_chk_guard == iVar1) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}

