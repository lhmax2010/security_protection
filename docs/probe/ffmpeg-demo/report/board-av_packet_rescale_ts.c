
void av_packet_rescale_ts
               (int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
               undefined4 param_5)

{
  int iVar1;
  int iVar2;
  undefined8 uVar3;
  
  if (*(int *)(param_1 + 0xc) == -0x80000000 && *(int *)(param_1 + 8) == 0) {
    iVar1 = *(int *)(param_1 + 0x10);
    iVar2 = *(int *)(param_1 + 0x14);
    if (iVar2 != -0x80000000 || iVar1 != 0) {
LAB_0020fb54:
      uVar3 = av_rescale_q(iVar1,iVar2,param_2,param_3,param_4,param_5);
      *(undefined8 *)(param_1 + 0x10) = uVar3;
      iVar1 = *(int *)(param_1 + 0x30);
      iVar2 = *(int *)(param_1 + 0x34);
      if (iVar2 < (int)(uint)(iVar1 == 0)) {
        return;
      }
      goto LAB_0020fb22;
    }
  }
  else {
    uVar3 = av_rescale_q(*(int *)(param_1 + 8),*(int *)(param_1 + 0xc),param_2,param_3,param_4,
                         param_5);
    *(undefined8 *)(param_1 + 8) = uVar3;
    iVar1 = *(int *)(param_1 + 0x10);
    iVar2 = *(int *)(param_1 + 0x14);
    if (iVar2 != -0x80000000 || iVar1 != 0) goto LAB_0020fb54;
  }
  iVar1 = *(int *)(param_1 + 0x30);
  iVar2 = *(int *)(param_1 + 0x34);
  if (iVar2 < (int)(uint)(iVar1 == 0)) {
    return;
  }
LAB_0020fb22:
  uVar3 = av_rescale_q(iVar1,iVar2,param_2,param_3,param_4,param_5);
  *(undefined8 *)(param_1 + 0x30) = uVar3;
  return;
}

