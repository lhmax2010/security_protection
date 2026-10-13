
void av_packet_rescale_ts
               (int param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
               undefined4 param_5)

{
  undefined8 uVar1;
  
  if (*(int *)(param_1 + 0xc) != -0x80000000 || *(int *)(param_1 + 8) != 0) {
    uVar1 = av_rescale_q(*(int *)(param_1 + 8),*(int *)(param_1 + 0xc),param_2,param_3,param_4,
                         param_5);
    *(undefined8 *)(param_1 + 8) = uVar1;
  }
  if (*(int *)(param_1 + 0x14) != -0x80000000 || *(int *)(param_1 + 0x10) != 0) {
    uVar1 = av_rescale_q(*(int *)(param_1 + 0x10),*(int *)(param_1 + 0x14),param_2,param_3,param_4,
                         param_5);
    *(undefined8 *)(param_1 + 0x10) = uVar1;
  }
  if ((int)(uint)(*(int *)(param_1 + 0x30) == 0) <= *(int *)(param_1 + 0x34)) {
    uVar1 = av_rescale_q(*(int *)(param_1 + 0x30),*(int *)(param_1 + 0x34),param_2,param_3,param_4,
                         param_5);
    *(undefined8 *)(param_1 + 0x30) = uVar1;
  }
  return;
}

