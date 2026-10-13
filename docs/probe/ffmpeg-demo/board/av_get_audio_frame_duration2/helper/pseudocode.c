
uint FUN_0023d794(char *param_1,uint param_2,uint param_3,int param_4,int param_5,uint param_6,
                 int param_7,int param_8,int param_9,uint param_10,uint param_11)

{
  int iVar1;
  uint uVar2;
  uint uVar3;
  char *pcVar4;
  int iVar5;
  bool bVar6;
  ulonglong uVar7;
  longlong lVar8;
  undefined8 uVar9;
  
  iVar1 = av_get_exact_bits_per_sample();
  uVar3 = 1;
  if ((0 < param_4) && (uVar2 = FUN_00275ad0(param_11,param_4), 1 < (int)uVar2)) {
    uVar3 = uVar2;
  }
  if (((0 < (int)param_11) && (param_3 - 1 < 0x7fff)) && (iVar1 != 0)) {
    uVar3 = FUN_002763b4(param_11 << 3,param_11 >> 0x1d,iVar1 * param_3,0);
    return uVar3;
  }
  if ((int)param_1 < 0x12001) {
    if ((int)param_1 < 0x11019) {
      if (param_1 == "") {
        return 0x40;
      }
      if (param_1 == "\x03") {
        return 0x20;
      }
    }
    else {
      if (param_1 == "\x02") {
        return 0x80;
      }
      if (param_1 == "L") {
        return 0xa0;
      }
    }
  }
  else {
    switch(param_1) {
    case (char *)0x15000:
    case "\x17":
      return 0x480;
    case "j-":
    case "-":
    case "\x17":
    case "":
    case "":
    case "":
    case (char *)0x15008:
    case "j-":
    case "-":
    case "":
    case "\x17":
    case "":
    case "":
    case "":
    case (char *)0x15010:
    case "j-":
    case "":
    case "\x17":
    case "":
    case "":
    case "":
    case "j-":
    case "-":
    case "":
    case "":
    case (char *)0x15020:
    case "j-":
    case "-":
    case "":
    case "\x17":
    case "":
    case "":
    case (char *)0x15028:
    case "j-":
    case "":
    case "\x17":
    case "":
    case "":
    case (char *)0x15030:
    case "j-":
    case "-":
    case "":
    case "\x17":
    case "":
    case "":
    case "":
    case (char *)0x15038:
    case "j-":
    case "-":
    case "":
    case "\x17":
    case "":
    case "":
    case "":
    case (char *)0x15040:
    case "j-":
    case "-":
    case "":
    case "\x17":
    case "":
    case "":
    case (char *)0x15048:
    case "j-":
    case "-":
    case "":
    case "\x17":
    case "":
    case "":
    case "":
    case (char *)0x15050:
    case "j-":
    case "-":
    case "":
    case "\x17":
    case "":
    case "":
    case "":
    case "j-":
    case "-":
    case "":
    case "\x17":
    case "":
    case "":
    case "":
    case (char *)0x15060:
    case "j-":
    case "-":
    case "":
      break;
    case "":
      return 0x600;
    case "-":
    case (char *)0x15018:
    case "":
      goto switchD_0023d7fe_caseD_15012;
    case "":
      return 0x140;
    case "":
    case (char *)0x15058:
      uVar2 = uVar3 << 10;
      if (uVar3 >> 0x15 != 0) {
        uVar2 = 0;
      }
      return uVar2;
    case "":
      return 0x800;
    case "-":
      return 0x180;
    case "":
      return 0x200;
    case "\x17":
      return 0x400;
    default:
      if (param_1 == "") {
        return 0x140;
      }
      if (param_1 == "ount_planes") {
        return 0xa0;
      }
    }
  }
  if (0 < (int)param_2) {
    if ((int)param_1 < 0x15030) {
      if (param_1 == "j-") {
        uVar3 = 0x480;
        if (param_2 < 0x5dc1) {
          uVar3 = 0x240;
        }
        return uVar3;
      }
      if (param_1 == "") {
        uVar3 = FUN_002763b4(param_2 << 8,param_2 >> 0x18,0xf5,0);
        return uVar3;
      }
    }
    else {
      if (param_1 == (char *)0x15030) {
        if (0x7bd0d < param_2) {
          return 0;
        }
        return 0x1e0 << (param_2 / 0x5622 & 0xff);
      }
      if (param_1 == "j-") {
        return param_2 / 0x4b;
      }
    }
  }
  if (0 < param_4) {
    if (param_1 == "") {
      if (param_4 == 0x26) {
switchD_0023d7fe_caseD_15012:
        return 0xa0;
      }
      if (param_4 == 0x32) {
        return 0xf0;
      }
    }
    else if (param_1 == "j-") {
      switch(param_4) {
      case 0x13:
        return 0x90;
      case 0x14:
        return 0xa0;
      case 0x1d:
        return 0x120;
      case 0x25:
        return 0x1e0;
      }
    }
  }
  if ((int)param_11 < 1) goto LAB_0023dfdc;
  if ((int)param_1 < 0x15021) {
    if (param_1 == "count_planes") {
      return (param_11 / 0x14) * 0xa0;
    }
    if (param_1 == "") {
      return ((param_11 >> 5) * 0x10 - (param_11 >> 5)) * 0x10;
    }
  }
  else {
    if (param_1 == "j-") {
      return (param_11 & 0x3fffffc0) << 2;
    }
    if (param_1 == "") {
      return param_11 & 0x7ffffffc;
    }
    if (param_1 == "") {
      return (uint)((ulonglong)param_11 * 0xaaaaaaab >> 0x20) & 0xfffffffc;
    }
  }
  if (0 < (int)param_6) {
    pcVar4 = "";
    if (param_1 != "") {
      pcVar4 = "";
    }
    if (param_1 == "" || param_1 == pcVar4) {
      uVar3 = FUN_00275858(param_11 << 3);
      return uVar3;
    }
  }
  if (0x7fffffd < param_3 - 1) goto LAB_0023dfdc;
  if (0x13fff < (int)param_1) {
    if ((int)param_1 < 0x1500a) {
      if ((int)param_1 < 0x14002) {
        if (param_1 == "avcodec_configuration") {
          uVar3 = FUN_00275ad0(param_11 - 8,param_3);
          return uVar3;
        }
        if (param_1 == "vcodec_configuration") {
          uVar3 = FUN_00275ad0((param_11 - param_3) + -6,param_3);
          return uVar3;
        }
      }
      else {
        if (param_1 == "codec_configuration") {
          uVar3 = FUN_00275ad0(param_11 + param_3 * -2,param_3);
          return uVar3;
        }
        if (param_1 == "j-") {
          uVar3 = FUN_00275858(param_11 * 3,param_3);
          return uVar3;
        }
      }
    }
    else if ((int)param_1 < 0x1503a) {
      if (param_1 == "-") {
        iVar1 = param_11 * 3;
        goto LAB_0023dea8;
      }
      if (param_1 == "") goto LAB_0023dd20;
    }
    else {
      if (param_1 == "-") {
LAB_0023dd20:
        uVar3 = FUN_00275858(param_11 << 2,param_3);
        return uVar3;
      }
      if (param_1 == "") {
        iVar1 = FUN_00275858(param_11,param_3 * 0x28);
        return iVar1 << 8;
      }
    }
    goto switchD_0023dba8_caseD_11006;
  }
  switch(param_1) {
  case "":
    uVar3 = FUN_00275ad0(param_11 * 2 + -8,param_3);
    return uVar3;
  case "":
  case "":
  case "":
  case "":
    uVar3 = FUN_00275ad0(param_11 * 2 + param_3 * -8,param_3);
    return uVar3;
  case "Z\x03":
    uVar3 = FUN_00275858(((param_11 >> 7) * 8 - (param_11 >> 7)) * 0x20,param_3);
    return uVar3;
  case "":
  case "\x12":
    if (param_9 != 0) {
      uVar3 = FUN_002763b4((int)((ulonglong)param_11 * 0xe),(int)((ulonglong)param_11 * 0xe >> 0x20)
                           ,param_3 << 3,0);
      return uVar3;
    }
    break;
  case "":
    return param_11 * 2 - 0x10;
  case "":
    iVar1 = FUN_00275858(param_11,param_3 * 9);
    return iVar1 << 4;
  case "":
  case "":
    uVar3 = FUN_00275858(param_11,param_3 << 4);
    uVar2 = uVar3 * 0x1c;
    if (0x4924924 < uVar3) {
      uVar2 = 0;
    }
    return uVar2;
  case "":
    iVar1 = FUN_00275ad0(param_11 + param_3 * -4,param_3 << 7);
    return iVar1 << 8;
  default:
    if (param_1 == "") {
      iVar1 = FUN_00275858(param_11,param_3 * 5);
      return iVar1 << 1;
    }
  case "":
  case "\x03":
  case "":
  case "":
  case "":
  case "":
  case "":
  case "":
  case "":
  case "":
  case "\x12":
  case "":
  case "":
  case "":
  case "e\x02":
  case "\x02":
  case "":
  case "":
  case "":
  case "":
  case "":
  case "":
  case "":
  case "":
  case "\t\x19":
  case "\x19":
  case "":
  case "":
  case "":
  case "":
  case "":
  case "":
  case "":
switchD_0023dba8_caseD_11006:
    if ((param_1 == "odec_configuration") && (param_5 != 0)) {
      if (param_5 != 3) {
        param_11 = param_11 << 1;
      }
      uVar3 = FUN_00275858(param_11,param_3);
      return uVar3;
    }
  }
  if (param_4 < 1) goto switchD_0023dd90_caseD_11004;
  uVar3 = FUN_00275858(param_11,param_4);
  switch(param_1) {
  case "":
    if (param_6 - 6 < 0xfffffffc) {
      return 0;
    }
    uVar2 = FUN_00275ad0(param_4 + param_3 * -4,param_6 * param_3);
    lVar8 = (ulonglong)(uVar2 * 8 + 1) * (ulonglong)uVar3;
    iVar1 = (int)lVar8;
    iVar5 = (((int)uVar2 >> 0x1f) << 3 | uVar2 >> 0x1d) * uVar3 + (int)((ulonglong)lVar8 >> 0x20);
    uVar7 = CONCAT44(iVar5,iVar1);
    if (iVar1 != 0 || iVar5 != 0) goto LAB_0023e08c;
    break;
  case "":
    lVar8 = FUN_00276314(param_4 * 2 - 0x20,-(uint)((uint)(param_4 * 2) < 0x20),3,0);
    lVar8 = lVar8 << 2;
    goto LAB_0023e074;
  case "":
    uVar9 = FUN_00276314(param_4 * 2 + param_3 * -8,
                         -(uint)((uint)(param_4 * 2) < param_3 * 8) - (param_3 >> 0x1d),param_3,0);
    iVar1 = (int)((ulonglong)uVar9 >> 0x20);
    bVar6 = 0xfffffffe < (uint)uVar9;
    uVar2 = (uint)uVar9 + 1;
    goto LAB_0023df7e;
  case "":
    lVar8 = ((ulonglong)param_3 * 0xfffffff9 + CONCAT44(-param_3,param_4)) * 2;
    uVar9 = FUN_00276314((int)lVar8,(int)((ulonglong)lVar8 >> 0x20),param_3,0);
    iVar1 = (int)((ulonglong)uVar9 >> 0x20);
    bVar6 = 0xfffffffd < (uint)uVar9;
    uVar2 = (uint)uVar9 + 2;
LAB_0023df7e:
    iVar5 = (int)((ulonglong)uVar2 * (ulonglong)uVar3);
    iVar1 = (iVar1 + (uint)bVar6) * uVar3 + (int)((ulonglong)uVar2 * (ulonglong)uVar3 >> 0x20);
    uVar7 = CONCAT44(iVar1,iVar5);
    if (iVar5 != 0 || iVar1 != 0) goto LAB_0023e08c;
    break;
  case "":
    lVar8 = CONCAT44(-(uint)((uint)(param_4 * 2) < param_3 * 8) - (param_3 >> 0x1d),
                     param_4 * 2 + param_3 * -8);
LAB_0023e074:
    uVar7 = FUN_00276314((int)lVar8,(int)((ulonglong)lVar8 >> 0x20),param_3,0);
    lVar8 = (uVar7 & 0xffffffff) * (ulonglong)uVar3;
    iVar1 = (int)lVar8;
    iVar5 = (int)(uVar7 >> 0x20) * uVar3 + (int)((ulonglong)lVar8 >> 0x20);
    uVar7 = CONCAT44(iVar5,iVar1);
    if (iVar1 != 0 || iVar5 != 0) {
LAB_0023e08c:
      uVar3 = (uint)uVar7;
      if ((int)(uVar7 >> 0x20) != (int)uVar3 >> 0x1f) {
        uVar3 = 0;
      }
      return uVar3;
    }
    break;
  case "\t\x19":
    lVar8 = (ulonglong)(param_4 * 2 - 0x20) * (ulonglong)uVar3;
    uVar7 = FUN_00276314((int)lVar8,
                         -(uint)((uint)(param_4 * 2) < 0x20) * uVar3 +
                         (int)((ulonglong)lVar8 >> 0x20),param_3,0);
    if (uVar7 != 0) goto LAB_0023e08c;
    break;
  case "":
    uVar2 = uVar3 << 5;
    uVar7 = (ulonglong)uVar2;
    goto joined_r0x0023df40;
  case "\x12":
    if (param_6 != 4) {
      return 0;
    }
    iVar1 = FUN_00275ad0(param_4 + param_3 * -4,param_3 << 2);
    uVar2 = uVar3 * iVar1 * 8;
    uVar7 = CONCAT44((int)(uVar3 * iVar1 * 8) >> 0x1f,uVar2);
joined_r0x0023df40:
    if (uVar2 != 0) goto LAB_0023e08c;
  }
switchD_0023dd90_caseD_11004:
  if (0 < (int)param_6) {
    if (param_1 == "") {
      iVar1 = FUN_00275858(param_11,param_6 + 4 >> 2);
LAB_0023dea8:
      uVar3 = FUN_00275858(iVar1 << 1,param_3);
      return uVar3;
    }
    if (param_1 == "") {
      if (param_6 < 4 || param_11 < 4) {
        return 0;
      }
      uVar3 = FUN_00275858(param_11 - 4,param_6 * (param_3 + 1 & 0xffffffe) >> 3);
      return uVar3;
    }
    if (param_1 == "") {
      if (param_6 < 4 || param_11 < 3) {
        return 0;
      }
      iVar1 = FUN_00275858(param_11 - 3,(param_6 >> 2) * param_3);
      return iVar1 << 1;
    }
  }
LAB_0023dfdc:
  if ((((int)param_10 < 2) || (param_11 == 0)) &&
     ((param_10 = 0, 0 < (int)param_2 && ((param_1 + -0x15007 < (char *)0x2 && (1 < param_4)))))) {
    uVar3 = (uint)(param_7 == 0);
    bVar6 = SBORROW4(param_8,uVar3);
    iVar1 = param_8 - (uint)(param_7 == 0);
    if ((int)uVar3 <= param_8) {
      bVar6 = SBORROW4(param_11,1);
      iVar1 = param_11 - 1;
    }
    if (iVar1 < 0 == bVar6) {
      lVar8 = (ulonglong)param_2 * (ulonglong)param_11 * 8;
      uVar3 = FUN_002763b4((int)lVar8,(int)((ulonglong)lVar8 >> 0x20));
      return uVar3;
    }
  }
  return param_10;
}

