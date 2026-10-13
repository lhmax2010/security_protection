
uint av_get_audio_frame_duration2(int param_1,undefined4 param_2)

{
  uint uVar1;
  
  uVar1 = FUN_0002c180(*(undefined4 *)(param_1 + 4),*(undefined4 *)(param_1 + 0x88),
                       *(undefined4 *)(param_1 + 0x74),*(undefined4 *)(param_1 + 0x8c),
                       *(undefined4 *)(param_1 + 8),*(undefined4 *)(param_1 + 0x28),
                       *(undefined4 *)(param_1 + 0x20),*(undefined4 *)(param_1 + 0x24),
                       *(undefined4 *)(param_1 + 0xc),*(undefined4 *)(param_1 + 0x90),param_2);
  return uVar1 & ~((int)uVar1 >> 0x1f);
}

