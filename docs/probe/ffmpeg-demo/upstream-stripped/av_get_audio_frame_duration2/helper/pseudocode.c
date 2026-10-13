
uint FUN_0002c180(char *param_1,uint param_2,uint param_3,uint param_4,int param_5,int param_6,
                 int param_7,int param_8,int param_9,uint param_10,uint param_11)

{
  int iVar1;
  uint uVar2;
  int iVar3;
  uint uVar4;
  uint uVar5;
  bool bVar6;
  undefined8 uVar7;
  longlong lVar8;
  
  uVar2 = param_4;
  iVar1 = av_get_exact_bits_per_sample();
  if ((int)param_4 < 1) {
    iVar3 = 1;
  }
  else {
    iVar3 = (int)param_11 / (int)param_4;
    if (iVar3 < 1) {
      iVar3 = 1;
    }
  }
  uVar5 = param_3 - 1;
  uVar4 = iVar1 - 1U;
  if (iVar1 - 1U < 0x7fff) {
    uVar4 = uVar5;
  }
  if (uVar4 < 0x7fff) {
    if (0 < (int)param_11) {
      uVar2 = FUN_0002e96c(param_11 << 3,((int)param_11 >> 0x1f) << 3 | param_11 >> 0x1d,
                           param_3 * iVar1,(int)(param_3 * iVar1) >> 0x1f,uVar2);
      return uVar2;
    }
    if (param_1 < "") goto LAB_0002c1d6;
    if (0 < (int)param_2) goto LAB_0002c2c8;
    if ((int)param_4 < 1) goto LAB_0002c55a;
LAB_0002c48c:
    if ((int)param_11 < 1) goto LAB_0002c55a;
    if (param_1 == "") goto LAB_0002c6aa;
    if (param_1 == (char *)0x15021) goto LAB_0002c602;
LAB_0002c4ae:
    if (param_1 == "") {
      return param_11 & 0xfffffffc;
    }
    if (param_1 == "") {
      return ((int)param_11 / 6) * 4;
    }
    if (0 < param_6) {
LAB_0002c6c8:
      if ((param_1 == "") || (param_1 == "")) {
        return (int)(param_11 << 3) / param_6;
      }
    }
LAB_0002c2f8:
    if (uVar5 < 0x7fffffe) {
      if ("\x01" < param_1) {
LAB_0002c63a:
        if (param_1 == (char *)0x15009) {
          return (int)(param_11 * 3) / (int)param_3;
        }
        goto LAB_0002c648;
      }
LAB_0002c314:
      if (":" < param_1) goto switchD_0002c32e_switchD;
      if (param_1 == "") {
        return (int)param_11 / (int)(param_3 * 5) << 1;
      }
      goto LAB_0002c77e;
    }
    goto LAB_0002c55a;
  }
  if (&__DT_REL[0x395].r_info < param_1) {
    if ((int)param_2 < 1) {
      if (0 < (int)param_4) goto LAB_0002c48c;
      if ((int)param_11 < 1) goto LAB_0002c55a;
      if (0 < param_6) goto LAB_0002c2f8;
      if (0x7fffffd < uVar5) goto LAB_0002c55a;
      goto LAB_0002c63a;
    }
LAB_0002c2c8:
    if ((int)param_4 < 1) {
      if ((int)param_11 < 1) goto LAB_0002c55a;
      if (param_1 == "") goto LAB_0002c6aa;
      goto LAB_0002c6f6;
    }
LAB_0002c2ce:
    if (param_1 != "") goto LAB_0002c5e4;
    if (param_4 == 0x26) {
LAB_0002c3e0:
      return 0xa0;
    }
    if (param_4 == 0x32) {
      return 0xf0;
    }
switchD_0002c942_caseD_15:
    if ((int)param_11 < 1) goto LAB_0002c55a;
    if (0 < param_6) goto LAB_0002c2f8;
    if (0x7fffffd < uVar5) goto LAB_0002c55a;
    if (param_1 < "") goto LAB_0002c314;
LAB_0002c648:
    if ((char *)0x15009 < param_1) {
      if (param_1 == "\x02") {
LAB_0002c87c:
        return (int)(param_11 << 2) / (int)param_3;
      }
      if (param_1 < "") {
        if (param_1 == "\x02") {
          return (int)(param_11 * 6) / (int)param_3;
        }
        if (param_1 == "") goto LAB_0002c87c;
      }
      else if (param_1 == "") {
        return (int)param_11 / (int)(param_3 * 0x28) << 8;
      }
      goto LAB_0002c77e;
    }
    if (param_1 == (char *)0x14001) {
      return (int)((param_11 - 6) - param_3) / (int)param_3;
    }
    if (param_1 == "\x02") {
      return (int)(param_11 + param_3 * -2) / (int)param_3;
    }
    if (param_1 == (char *)0x14000) {
      return (int)(param_11 - 8) / (int)param_3;
    }
  }
  else {
LAB_0002c1d6:
    if ("" < param_1) {
      switch(param_1) {
      case (char *)0x15000:
      case "\x17":
        return 0x480;
      case "":
        return 0x600;
      case "\x02":
      case (char *)0x15018:
      case "":
        goto LAB_0002c3e0;
      case "":
        return 0x140;
      case "":
      case (char *)0x15058:
        if (0x1fffff < iVar3) {
          return 0;
        }
        return iVar3 << 10;
      case "":
        return 0x800;
      case "\x02":
        return 0x180;
      case "":
        return 0x200;
      case "\x17":
        return 0x400;
      }
      if (0 < (int)param_2) {
        if (param_1 == "") {
          uVar2 = FUN_0002e96c(param_2 << 8,((int)param_2 >> 0x1f) << 8 | param_2 >> 0x18,0xf5,0,
                               uVar2);
          return uVar2;
        }
        if (param_1 == (char *)0x15051) {
          return (int)param_2 / 0x4b;
        }
        if (param_1 == (char *)0x15030) {
          if (0x7bd0d < (int)param_2) {
            return 0;
          }
          return 0x1e0 << ((int)param_2 / 0x5622 & 0xffU);
        }
LAB_0002c3f4:
        if (param_1 == (char *)0x15001) {
          if ((int)param_2 < 0x5dc1) {
            return 0x240;
          }
          return 0x480;
        }
      }
      if (0 < (int)param_4) {
        if (param_1 != (char *)0x15029) goto LAB_0002c2ce;
        switch(param_4) {
        case 0x13:
          return 0x90;
        case 0x14:
          goto LAB_0002c3e0;
        case 0x1d:
          return 0x120;
        case 0x25:
          return 0x1e0;
        }
        goto switchD_0002c942_caseD_15;
      }
LAB_0002c5e4:
      if (0 < (int)param_11) {
        if (param_1 == "") {
LAB_0002c6aa:
          return ((int)param_11 >> 5) * 0xf0;
        }
LAB_0002c5f6:
        if (param_1 == (char *)0x15021) {
LAB_0002c602:
          return ((int)param_11 >> 6) << 8;
        }
LAB_0002c6f6:
        if (param_1 == "e_free") {
          return ((int)param_11 / 0x14) * 0xa0;
        }
        goto LAB_0002c4ae;
      }
      goto LAB_0002c55a;
    }
    if (param_1 == "") {
      return 0x20;
    }
    if (param_1 < "\f") {
      if (param_1 == (char *)0x11000) {
        return 0x40;
      }
      if (0 < (int)param_2) goto LAB_0002c3f4;
      if ((int)param_4 < 1) {
        if (0 < (int)param_11) {
          if (0 < param_6) goto LAB_0002c2f8;
          if (uVar5 < 0x7fffffe) goto LAB_0002c314;
        }
      }
      else {
LAB_0002c688:
        if (0 < (int)param_11) goto LAB_0002c4ae;
      }
      goto LAB_0002c55a;
    }
    if (param_1 == "") {
      return 0x80;
    }
    if ("\x12" < param_1) {
      if (param_1 == "ray_add_nofree") {
        return 0x140;
      }
      if (param_1 == "_free") {
        return 0xa0;
      }
      if (param_1 == "rray_add_nofree") {
        return 0xa0;
      }
      if ((int)param_4 < 1) {
        if (0 < (int)param_11) goto LAB_0002c6f6;
        goto LAB_0002c55a;
      }
      goto LAB_0002c5e4;
    }
    if (0 < (int)param_2) {
      if (0 < (int)param_4) goto LAB_0002c5e4;
      if ((int)param_11 < 1) goto LAB_0002c55a;
      goto LAB_0002c5f6;
    }
    if (0 < (int)param_4) goto LAB_0002c688;
    if ((int)param_11 < 1) goto LAB_0002c55a;
    if (0 < param_6) goto LAB_0002c6c8;
    if (0x7fffffd < uVar5) goto LAB_0002c55a;
switchD_0002c32e_switchD:
    switch(param_1) {
    case "":
      return (int)((param_11 - 4) * 2) / (int)param_3;
    case "":
    case "":
    case "":
    case "\x01":
      return (int)((param_11 + param_3 * -4) * 2) / (int)param_3;
    case "\x12":
      return (((int)param_11 >> 7) * 0xe0) / (int)param_3;
    case "":
    case "H":
      if (param_9 != 0) {
        uVar2 = FUN_0002e96c((int)((longlong)(int)param_11 * 0xe),
                             (int)((ulonglong)((longlong)(int)param_11 * 0xe) >> 0x20),param_3 << 3,
                             (int)(param_3 << 3) >> 0x1f,uVar2);
        return uVar2;
      }
      goto LAB_0002c77e;
    case "":
      return (param_11 - 8) * 2;
    case "":
      return (int)param_11 / (int)(param_3 * 9) << 4;
    case "#\x01":
    case "":
      iVar1 = (int)param_11 / (int)(param_3 << 4);
      if (0x4924924 < iVar1) {
        return 0;
      }
      return iVar1 * 0x1c;
    case "r\x01":
      return (int)(param_11 + param_3 * -4) / (int)(param_3 << 7) << 8;
    }
  }
  if ((param_1 == "") && (param_5 != 0)) {
    if (param_5 != 3) {
      param_11 = param_11 << 1;
    }
    return (int)param_11 / (int)param_3;
  }
LAB_0002c77e:
  if (((int)param_4 < 1) ||
     (uVar4 = (int)param_11 / (int)param_4, (char *)0x33 < param_1 + -0x11001)) {
switchD_0002c792_caseD_11004:
    if (0 < param_6) {
      if (param_1 == "") {
        if (param_6 < 4) {
          return 0;
        }
        if ((int)param_11 < 4) {
          return 0;
        }
        return (param_11 - 4) / (uint)((int)(param_6 * (param_3 + 1 & 0xfffffffe)) >> 3);
      }
      if (param_1 == "") {
        return ((int)param_11 / (param_6 + 4 >> 2) << 1) / (int)param_3;
      }
      if (param_1 == "") {
        if (param_6 < 4) {
          return 0;
        }
        if ((int)param_11 < 3) {
          return 0;
        }
        return (param_11 - 3) / (param_3 * (param_6 >> 2)) << 1;
      }
    }
    goto LAB_0002c55a;
  }
  iVar1 = (int)param_4 >> 0x1f;
  iVar3 = (int)param_3 >> 0x1f;
  switch(param_1) {
  case "k\x01":
    if (3 < param_6 - 2U) {
      return 0;
    }
    lVar8 = (longlong)((int)(param_4 + param_3 * -4) / (int)(param_6 * param_3)) * 8 + 1;
    break;
  case "\x01":
    uVar5 = param_4 - 0x10;
    lVar8 = FUN_0002e96c(uVar5 * 2,
                         (iVar1 + -1 + (uint)(0xf < param_4)) * 2 + (uint)CARRY4(uVar5,uVar5),3,0,
                         uVar2);
    lVar8 = FUN_0002e96c((int)(lVar8 << 2),(int)((ulonglong)(lVar8 << 2) >> 0x20),param_3,iVar3);
    break;
  case "":
    uVar5 = param_4 + param_3 * -4;
    uVar7 = FUN_0002e96c(uVar5 * 2,
                         ((iVar1 - (iVar3 << 2 | param_3 >> 0x1e)) - (uint)(param_4 < param_3 * 4))
                         * 2 + (uint)CARRY4(uVar5,uVar5),param_3,iVar3,uVar2);
    iVar1 = (int)((ulonglong)uVar7 >> 0x20);
    bVar6 = 0xfffffffe < (uint)uVar7;
    iVar3 = (uint)uVar7 + 1;
    goto LAB_0002cab0;
  default:
    goto switchD_0002c792_caseD_11004;
  case "":
    lVar8 = (longlong)(int)param_3 * -7 + (longlong)(int)param_4;
    uVar5 = (uint)lVar8;
    uVar7 = FUN_0002e96c(uVar5 * 2,(int)((ulonglong)lVar8 >> 0x20) * 2 + (uint)CARRY4(uVar5,uVar5),
                         param_3,iVar3,uVar2);
    iVar1 = (int)((ulonglong)uVar7 >> 0x20);
    bVar6 = 0xfffffffd < (uint)uVar7;
    iVar3 = (uint)uVar7 + 2;
LAB_0002cab0:
    lVar8 = CONCAT44(iVar1 + (uint)bVar6,iVar3);
    break;
  case "\x01":
    uVar5 = param_4 + param_3 * -4;
    lVar8 = FUN_0002e96c(uVar5 * 2,
                         ((iVar1 - (iVar3 << 2 | param_3 >> 0x1e)) - (uint)(param_4 < param_3 * 4))
                         * 2 + (uint)CARRY4(uVar5,uVar5),param_3,iVar3,uVar2);
    break;
  case "\x12":
    lVar8 = (ulonglong)(param_4 - 0x10) * (ulonglong)uVar4;
    uVar5 = (uint)lVar8;
    lVar8 = FUN_0002e96c(uVar5 * 2,
                         (uVar4 * (iVar1 + -1 + (uint)(0xf < param_4)) +
                          (param_4 - 0x10) * ((int)uVar4 >> 0x1f) + (int)((ulonglong)lVar8 >> 0x20))
                         * 2 + (uint)CARRY4(uVar5,uVar5),param_3,iVar3,uVar2);
    goto LAB_0002ca18;
  case "":
    lVar8 = CONCAT44((int)(uVar4 << 5) >> 0x1f,uVar4 << 5);
    goto LAB_0002ca18;
  case "<":
    if (param_6 != 4) {
      return 0;
    }
    iVar1 = uVar4 * ((int)(param_4 + param_3 * -4) / (int)(param_3 << 2));
    lVar8 = CONCAT44(iVar1 * 8 >> 0x1f,iVar1 * 8);
    goto LAB_0002ca18;
  }
  lVar8 = lVar8 * (int)uVar4;
LAB_0002ca18:
  if (lVar8 == 0) {
LAB_0002c55a:
    bVar6 = param_11 != 0;
    iVar1 = 0;
    if (bVar6) {
      iVar1 = param_10 - 1;
    }
    if ((bVar6 && param_10 != 1) && iVar1 < 0 == (bVar6 && SBORROW4(param_10,1))) {
      return param_10;
    }
    if ((int)param_11 < 1 || param_8 < (int)(uint)(param_7 == 0)) {
      return 0;
    }
    bVar6 = param_2 == 0;
    uVar4 = param_2;
    if (0 < (int)param_2) {
      uVar4 = param_4 - 1;
      bVar6 = param_4 == 1;
    }
    if (bVar6 || (int)uVar4 < 0 != (0 < (int)param_2 && SBORROW4(param_4,1))) {
      return 0;
    }
    if (param_1 + -0x15007 < (char *)0x2) {
      lVar8 = (longlong)(int)param_11 * (longlong)(int)param_2 * 8;
      uVar2 = FUN_0002e96c((int)lVar8,(int)((ulonglong)lVar8 >> 0x20),param_7,param_8,uVar2);
      return uVar2;
    }
  }
  else if ((int)((ulonglong)lVar8 >> 0x20) == (int)(uint)lVar8 >> 0x1f) {
    return (uint)lVar8;
  }
  return 0;
}

