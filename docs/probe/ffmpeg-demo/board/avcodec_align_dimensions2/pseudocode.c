
void avcodec_align_dimensions2(int param_1,uint *param_2,uint *param_3,undefined4 *param_4)

{
  undefined1 auVar1 [16];
  int iVar2;
  int iVar3;
  uint uVar4;
  int iVar5;
  
  iVar2 = av_pix_fmt_desc_get(*(undefined4 *)(param_1 + 0x74));
  iVar5 = 1;
  if (iVar2 == 0) {
    iVar3 = 1;
    uVar4 = *(uint *)(param_1 + 0x74);
  }
  else {
    iVar3 = 1 << *(sbyte *)(iVar2 + 6);
    iVar5 = 1 << *(sbyte *)(iVar2 + 5);
    uVar4 = *(uint *)(param_1 + 0x74);
  }
  if (0xbb < uVar4) goto switchD_0023d18e_caseD_9;
  switch(uVar4) {
  default:
    iVar5 = 0x10;
    if (*(int *)(param_1 + 0x10) == 0x87) {
      iVar5 = 0x20;
    }
    goto LAB_0023d314;
  case 2:
    if (*(int *)(param_1 + 0x10) == 0x2b) {
      iVar3 = 4;
      iVar5 = 4;
    }
    break;
  case 3:
    if (*(int *)(param_1 + 0x10) - 0x35U < 2) {
      iVar3 = 4;
      iVar5 = 4;
    }
    break;
  case 6:
    if (*(int *)(param_1 + 0x10) == 0x16) {
      iVar5 = 0x40;
      iVar3 = 0x40;
    }
    else if (*(int *)(param_1 + 0x10) == 0xd0) {
      iVar5 = 0x10;
      iVar3 = 0x10;
    }
    break;
  case 7:
  case 0x10:
  case 0x8a:
    iVar5 = 0x20;
LAB_0023d314:
    iVar3 = 0x20;
    break;
  case 9:
  case 10:
  case 0x12:
  case 0x13:
  case 0x15:
  case 0x16:
  case 0x17:
  case 0x18:
  case 0x19:
  case 0x1a:
  case 0x1b:
  case 0x1c:
  case 0x22:
  case 0x23:
  case 0x24:
  case 0x25:
  case 0x26:
  case 0x28:
  case 0x29:
  case 0x2a:
  case 0x2b:
  case 0x2c:
  case 0x33:
  case 0x34:
  case 0x35:
  case 0x36:
  case 0x37:
  case 0x38:
  case 0x39:
  case 0x3a:
  case 0x62:
  case 99:
  case 100:
  case 0x65:
  case 0x66:
  case 0x67:
  case 0x68:
  case 0x69:
  case 0x6a:
  case 0x6b:
  case 0x6d:
  case 0x6e:
  case 0x72:
  case 0x73:
  case 0x74:
  case 0x75:
  case 0x76:
  case 0x77:
  case 0x78:
  case 0x8b:
  case 0x8c:
  case 0x8d:
  case 0x8e:
  case 0x8f:
  case 0x90:
  case 0x91:
  case 0x92:
  case 0x93:
  case 0x94:
  case 0x95:
  case 0x96:
  case 0x9b:
  case 0x9c:
  case 0x9d:
  case 0x9e:
  case 0x9f:
  case 0xa2:
  case 0xa3:
  case 0xa4:
  case 0xa5:
  case 0xa6:
  case 0xa7:
  case 0xa8:
  case 0xa9:
  case 0xaa:
  case 0xab:
  case 0xac:
  case 0xad:
  case 0xae:
  case 0xaf:
  case 0xb0:
  case 0xb1:
  case 0xb2:
  case 0xb3:
  case 0xb4:
  case 0xb5:
  case 0xb6:
  case 0xb7:
    break;
  case 0xb:
  case 0x11:
  case 0x14:
    iVar2 = *(int *)(param_1 + 0x10);
    if (iVar2 == 0x31 || iVar2 == 0x2b) {
      iVar5 = 4;
      iVar3 = 4;
    }
    if ((iVar2 == 0x27 || iVar2 == 0xfc) || (iVar2 == 0x94)) {
      iVar5 = 8;
      iVar3 = 8;
    }
    if ((iVar2 - 7U < 5) || (iVar2 == 0xd1 || iVar2 == 0x6b)) {
      iVar3 = 0x10;
      iVar5 = 8;
    }
    break;
  case 0x27:
    if (*(int *)(param_1 + 0x10) == 0x2a) {
      iVar5 = 4;
      iVar3 = 4;
    }
    if (*(int *)(param_1 + 0x10) == 0x27) {
      iVar3 = 8;
      iVar5 = 8;
    }
    break;
  case 0x79:
    if (*(int *)(param_1 + 0x10) == 0xfc) {
      iVar3 = 8;
      iVar5 = 8;
    }
  }
switchD_0023d18e_caseD_9:
  iVar2 = iVar5;
  if (iVar5 < 0x11) {
    iVar2 = 0x10;
  }
  if (*(int *)(param_1 + 0x10) != 0x88) {
    iVar2 = iVar5;
  }
  *param_2 = (iVar2 + *param_2) - 1 & -iVar2;
  uVar4 = (*param_3 + iVar3) - 1 & -iVar3;
  *param_3 = uVar4;
  iVar5 = *(int *)(param_1 + 0x10);
  if ((((iVar5 == 0x1b) || (*(int *)(param_1 + 0x280) != 0)) ||
      ((iVar5 - 0x5aU < 0x11 && ((1 << (iVar5 - 0x5aU & 0xff) & 0x10007U) != 0)))) ||
     (iVar5 - 0x46U < 2)) {
    *param_3 = uVar4 + 2;
    uVar4 = *param_2;
    if ((int)uVar4 < 0x21) {
      uVar4 = 0x20;
    }
    *param_2 = uVar4;
    iVar5 = *(int *)(param_1 + 0x10);
  }
  if (iVar5 == 0x17) {
    uVar4 = *param_2;
    if ((int)uVar4 < 0x21) {
      uVar4 = 0x20;
    }
    *param_2 = uVar4;
  }
  auVar1._8_8_ = SUB128(SUB1612((undefined1  [16])0x0,4),4);
  auVar1._0_8_ = 0x1000000010;
  auVar1 = auVar1 << 0x40 | auVar1;
  *param_4 = *(undefined4 *)auVar1;
  param_4[1] = *(undefined4 *)(auVar1 + (undefined1  [16])0x4);
  param_4[2] = *(undefined4 *)(auVar1 + (undefined1  [16])0x8);
  param_4[3] = *(undefined4 *)(auVar1 + (undefined1  [16])0xc);
  return;
}

