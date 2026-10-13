
void avcodec_align_dimensions2(int param_1,uint *param_2,uint *param_3,undefined4 *param_4)

{
  undefined1 auVar1 [16];
  int iVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  uint uVar6;
  uint uVar7;
  
  iVar2 = __stack_chk_guard;
  iVar3 = av_pix_fmt_desc_get(*(undefined4 *)(param_1 + 0x74),param_2,&__DT_PLTGOT,0);
  if (iVar3 == 0) {
    iVar5 = 1;
    iVar3 = iVar5;
  }
  else {
    iVar5 = 1 << *(sbyte *)(iVar3 + 5);
    iVar3 = 1 << *(sbyte *)(iVar3 + 6);
  }
  uVar6 = *(uint *)(param_1 + 0x74);
  iVar4 = *(int *)(param_1 + 0x10);
  if ((int)uVar6 < 0x12) {
    if ((int)uVar6 < 7) {
      if (uVar6 < 7) {
        switch(uVar6) {
        case 2:
          if (iVar4 == 0x2b) {
LAB_0031f4d2:
            uVar6 = 0xfffffffc;
            iVar3 = 4;
            uVar7 = 0xfffffffc;
            iVar5 = 4;
            goto LAB_0031f412;
          }
          break;
        case 3:
          if (iVar4 - 0x35U < 2) goto LAB_0031f4d2;
          break;
        default:
          goto switchD_0031f274_caseD_4;
        case 6:
          if (iVar4 == 0x16) {
            uVar6 = 0xffffffc0;
            iVar3 = 0x40;
            uVar7 = 0xffffffc0;
            iVar5 = 0x40;
            goto LAB_0031f412;
          }
          if (iVar4 == 0xd0) {
            uVar6 = 0xfffffff0;
            iVar3 = 0x10;
            uVar7 = 0xfffffff0;
            iVar5 = 0x10;
            goto LAB_0031f412;
          }
        }
      }
    }
    else {
      uVar6 = 1 << (uVar6 & 0xff);
      if ((uVar6 & 0xf100) != 0) goto switchD_0031f274_caseD_4;
      if ((uVar6 & 0x10080) != 0) goto switchD_0031f290_caseD_8a;
      if ((uVar6 & 0x20800) != 0) goto switchD_0031f290_caseD_14;
    }
    goto switchD_0031f290_caseD_15;
  }
  switch(uVar6) {
  case 0x14:
switchD_0031f290_caseD_14:
    if (iVar4 == 0x2b || iVar4 == 0x31) {
      iVar3 = 4;
      uVar6 = 0xfffffffc;
      iVar5 = 4;
      goto LAB_0031f410;
    }
    if (iVar4 == 0x27 || (iVar4 == 0xfc || iVar4 == 0x94)) goto LAB_0031f502;
    if ((iVar4 == 0x6b || iVar4 == 0xd1) || (iVar4 - 7U < 5)) {
      uVar6 = 0xfffffff0;
      uVar7 = 0xfffffff8;
      iVar3 = 0x10;
      iVar5 = 8;
      goto LAB_0031f412;
    }
    break;
  case 0x1d:
  case 0x1e:
  case 0x1f:
  case 0x20:
  case 0x21:
  case 0x2d:
  case 0x2e:
  case 0x2f:
  case 0x30:
  case 0x31:
  case 0x32:
  case 0x3b:
  case 0x3c:
  case 0x3d:
  case 0x3e:
  case 0x3f:
  case 0x40:
  case 0x41:
  case 0x42:
  case 0x43:
  case 0x44:
  case 0x45:
  case 0x46:
  case 0x47:
  case 0x48:
  case 0x49:
  case 0x4a:
  case 0x4b:
  case 0x4c:
  case 0x4d:
  case 0x4e:
  case 0x4f:
  case 0x50:
  case 0x51:
  case 0x52:
  case 0x53:
  case 0x54:
  case 0x55:
  case 0x56:
  case 0x57:
  case 0x58:
  case 0x59:
  case 0x5a:
  case 0x5b:
  case 0x5c:
  case 0x5d:
  case 0x5e:
  case 0x5f:
  case 0x60:
  case 0x61:
  case 0x6c:
  case 0x6f:
  case 0x70:
  case 0x71:
  case 0x7a:
  case 0x7b:
  case 0x7c:
  case 0x7d:
  case 0x7e:
  case 0x7f:
  case 0x80:
  case 0x81:
  case 0x82:
  case 0x83:
  case 0x84:
  case 0x85:
  case 0x86:
  case 0x87:
  case 0x88:
  case 0x89:
  case 0x97:
  case 0x98:
  case 0x99:
  case 0x9a:
  case 0xa0:
  case 0xa1:
  case 0xb8:
  case 0xb9:
  case 0xba:
  case 0xbb:
switchD_0031f274_caseD_4:
    uVar6 = 0xffffffe0;
    iVar3 = 0x20;
    iVar5 = 0x20;
    if (iVar4 != 0x87) {
      iVar5 = 0x10;
      goto LAB_0031f406;
    }
    goto LAB_0031f410;
  case 0x27:
    if (iVar4 == 0x2a) goto LAB_0031f4d2;
    if (iVar4 == 0x27) goto LAB_0031f502;
    break;
  case 0x79:
    if (iVar4 == 0xfc) {
LAB_0031f502:
      uVar6 = 0xfffffff8;
      iVar5 = 8;
      iVar3 = iVar5;
      uVar7 = uVar6;
      goto LAB_0031f412;
    }
    break;
  case 0x8a:
switchD_0031f290_caseD_8a:
    iVar5 = 0x20;
    uVar6 = 0xffffffe0;
    iVar3 = iVar5;
    goto LAB_0031f406;
  }
switchD_0031f290_caseD_15:
  uVar6 = -iVar3;
LAB_0031f406:
  if ((iVar4 == 0x88) && (iVar5 < 0x10)) {
    iVar5 = 0x10;
  }
LAB_0031f410:
  uVar7 = -iVar5;
LAB_0031f412:
  *param_2 = (*param_2 - 1) + iVar5 & uVar7;
  uVar6 = (*param_3 - 1) + iVar3 & uVar6;
  *param_3 = uVar6;
  iVar3 = *(int *)(param_1 + 0x10);
  if ((iVar3 == 0x1b) ||
     (iVar3 - 0x5aU < 3 || (iVar3 - 0x46U < 2 || (*(int *)(param_1 + 0x280) != 0 || iVar3 == 0x6a)))
     ) {
    *param_3 = uVar6 + 2;
    uVar6 = *param_2;
    if ((int)uVar6 < 0x20) {
      uVar6 = 0x20;
    }
    *param_2 = uVar6;
    iVar3 = *(int *)(param_1 + 0x10);
  }
  if (iVar3 == 0x17) {
    uVar6 = *param_2;
    if ((int)uVar6 < 0x20) {
      uVar6 = 0x20;
    }
    *param_2 = uVar6;
  }
  auVar1._8_8_ = SUB128(SUB1612((undefined1  [16])0x0,4),4);
  auVar1._0_8_ = 0x1000000010;
  auVar1 = auVar1 << 0x40 | auVar1;
  *param_4 = *(undefined4 *)auVar1;
  param_4[1] = *(undefined4 *)(auVar1 + (undefined1  [16])0x4);
  param_4[2] = *(undefined4 *)(auVar1 + (undefined1  [16])0x8);
  param_4[3] = *(undefined4 *)(auVar1 + (undefined1  [16])0xc);
  if (__stack_chk_guard != iVar2) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}

