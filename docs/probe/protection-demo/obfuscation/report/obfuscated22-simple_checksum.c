
uint simple_checksum(byte *param_1)

{
  uint uVar1;
  uint uVar2;
  uint uVar3;
  int iVar4;
  uint uVar5;
  uint *puVar6;
  byte *pbVar7;
  uint uVar8;
  uint uVar9;
  uint uVar10;
  uint uVar11;
  uint uVar12;
  uint uVar13;
  uint *puVar14;
  uint uVar15;
  uint uVar16;
  bool bVar17;
  uint local_8c;
  uint local_84;
  uint local_80;
  uint local_7c;
  byte *local_78;
  uint local_74;
  uint local_70;
  uint local_6c;
  undefined1 uStack_60;
  undefined1 uStack_5f;
  undefined1 uStack_5e;
  undefined1 uStack_5d;
  undefined1 uStack_5c;
  undefined1 uStack_5b;
  undefined1 uStack_5a;
  undefined1 uStack_59;
  undefined1 uStack_58;
  undefined1 uStack_57;
  undefined1 uStack_56;
  undefined1 auStack_55 [33];
  uint local_34 [2];
  uint uStack_2c;
  undefined1 uStack_25;
  
  uVar1 = (uint)&uStack_25 ^ 0xe94b27c1;
  uVar2 = (uint)&uStack_5b ^ 0xda2123bc;
  uVar15 = (uint)&uStack_25 ^ 0x97c7a440;
  uVar10 = (uint)&uStack_25 ^ 0x97c7a440;
  local_8c = 0;
  puVar6 = local_34;
  if ((uVar10 * 0x3b647080 ^ uVar10 * 0x1076c8e1 >> 0xd) !=
      (uVar15 * 0x3b647080 ^ uVar15 * 0x1076c8e1 >> 0xd) + 1) {
    puVar6 = &uStack_2c;
  }
  *puVar6 = 0x638ddd20;
  uVar10 = (uint)&uStack_5c ^ 0x893b8033;
  uVar15 = (uint)&uStack_5e ^ 0x3607f5e8;
  uVar8 = (uint)&uStack_5d ^ 0x50e64053;
  uVar5 = (uint)&uStack_5d ^ 0xaf19bfac;
  uVar3 = ((uint)&uStack_59 & 3) + 1;
  local_74 = 0;
  local_7c = 0;
  local_6c = 0;
  local_80 = 0;
  local_70 = 0;
  local_84 = 0;
  local_78 = param_1;
  do {
    uVar9 = (uint)&uStack_25 ^ 0xf271e46f;
    uVar11 = (uint)&uStack_25 ^ 0xf271e46f;
    uVar13 = uVar9 + 0x67584a3f;
    uVar12 = uVar11 + 0x67584a3f;
    puVar6 = local_34;
    if ((uVar13 ^ uVar9) * 0x67584a3f + uVar13 != (uVar12 ^ uVar11) * 0x67584a3f + uVar12 + 1) {
      puVar6 = &uStack_2c;
    }
    uVar9 = ((*puVar6 ^ 0xea9bcfa) * -0x1339ee29 + 0xd7bebf39) % 3;
    puVar6 = local_34;
    if (uVar9 == 0) {
      uVar9 = uVar1 + 0x14fe39cd ^ 0xff901406;
      uVar11 = uVar1 + 0x14fe39cd ^ 0xff901406;
      puVar14 = &uStack_2c;
      if ((uVar9 * 0x716e5800 | uVar9 * -0x1491d235 >> 0x15) ==
          uVar11 * 0x716e5800 + (uVar11 * -0x1491d235 >> 0x15) + 1) {
        puVar14 = local_34;
      }
      uVar9 = (*puVar14 ^ 0x8a922faa) * -0x5d168c13 + 0xc0b81ad5;
      uVar9 = uVar9 >> 7 | uVar9 * 0x2000000;
      if ((int)uVar9 < 0x343692ab) {
        if (uVar9 != 0x99779408) {
          if (uVar9 != 0xa0efbe92) {
            uVar13 = uVar2 ^ (uint)&uStack_58 ^ 0xb67c20c1;
            uVar16 = uVar13 + 0xc4c8f8fa;
            uVar11 = uVar1 + 0x9667abb0 ^ 0x63b170b6;
            uVar12 = uVar1 + 0x9667abb0 ^ 0x63b170b6;
            uVar9 = 0xccd06f57;
            if (((uVar16 ^ uVar13) * 0x8f8fb + uVar16 & 0x100000) == 0) {
              uVar9 = 0x5fa9f76c;
            }
            uVar12 = uVar12 * -0x4927c800 | uVar12 * -0xa2924f9 >> 0x15;
            iVar4 = uVar11 * -0x4927c800 + (uVar11 * -0xa2924f9 >> 0x15);
            goto LAB_00010b00;
          }
          uVar9 = 0xb504eade;
          uVar11 = uVar1 + 0xe248b463 ^ 0x1912b624;
          uVar12 = uVar1 + 0xe248b463 ^ 0x1912b624;
          uVar11 = uVar11 * -0x2fedc800 | uVar11 * -0x4a5fdb9 >> 0x15;
          uVar12 = uVar12 * -0x2fedc800 + (uVar12 * -0x4a5fdb9 >> 0x15);
          goto LAB_000111dc;
        }
        uVar11 = (uint)&uStack_25 ^ 0x78f8b86d;
        uVar12 = (uint)&uStack_25 ^ 0x78f8b86d;
        uVar13 = uVar12 + 0xa3dfa50f;
        uVar16 = uVar11 + 0xa3dfa50f;
        uVar9 = 0x13d3e5c3;
        if ((uVar16 ^ uVar11) * -0x5c205af1 + uVar16 != (uVar13 ^ uVar12) * -0x5c205af1 + uVar13 + 1
           ) {
          puVar6 = &uStack_2c;
        }
        local_6c = 0;
        local_80 = ((uint)auStack_55 & 3) + 1;
      }
      else if ((int)uVar9 < 0x72f12806) {
        if (uVar9 == 0x343692ab) {
          local_74 = local_74 + 1;
          uVar16 = (uint)&uStack_25 ^ 0x4fcc37de;
          uVar11 = uVar16 + 0xce30dec1;
          uVar12 = (uint)&uStack_25 ^ 0x4fcc37de;
          uVar13 = uVar12 + 0xce30dec1;
          uVar9 = 0xd6a2600;
          if (local_74 < local_7c) {
            uVar9 = 0x9c0a9893;
          }
          if ((uVar11 ^ uVar16) * -0x31cf213f + uVar11 !=
              (uVar13 ^ uVar12) * -0x31cf213f + uVar13 + 1) {
            puVar6 = &uStack_2c;
          }
        }
        else {
          uVar11 = (uint)&uStack_25 ^ 0x949e441;
          uVar12 = uVar11 + 0x5472bac2;
          uVar13 = (uint)&uStack_25 ^ 0x949e441;
          uVar9 = 0xf0b55516;
          local_70 = 0;
          local_84 = uVar3;
          if ((uVar12 ^ uVar11) * 0x5472bac3 + uVar12 !=
              (uVar13 + 0x5472bac2 ^ uVar13) * 0x5472bac3 + uVar13 + 0x5472bac3) {
            puVar6 = &uStack_2c;
          }
        }
      }
      else if (uVar9 == 0x72f12806) {
        pbVar7 = local_78 + 1;
        uVar9 = local_8c * 0x1f + (uint)*local_78;
        uVar9 = (uint)&uStack_5f ^ 0x4ee7313 ^
                (((uint)&uStack_5f ^ 0x672037c5) & ~uVar9 | uVar9 & ((uint)&uStack_5f ^ 0x98dfc83a))
                ^ 0x9c31bb29;
        uVar11 = (uVar5 & ~uVar9 | uVar9 & uVar8) ^ (uVar5 & 0xffff) + (uVar8 & 0xffff0000) |
                 uVar9 & 0xffff0000;
        uVar12 = (uint)&uStack_60 ^ 0xca2c29bb;
        uVar9 = 0x638ddd20;
        uVar13 = (uint)&uStack_25 ^ 0xeea65fff;
        uVar16 = uVar13 + 0xd641aa22;
        local_8c = ((((uint)&uStack_5c ^ 0x76c47fcc) & ~uVar11 | uVar11 & uVar10) ^ uVar10) &
                   ((((uint)&uStack_60 ^ 0x35d3d644) & ((uint)&uStack_5e ^ 0xc9f80a17) |
                    uVar12 & uVar15) ^ uVar15 | uVar12);
        uVar11 = (uint)&uStack_25 ^ 0xeea65fff;
        local_78 = pbVar7;
        if ((uVar16 ^ uVar13) * -0x29be55dd + uVar16 !=
            (uVar11 + 0xd641aa22 ^ uVar11) * -0x29be55dd + uVar11 + 0xd641aa23) {
          puVar6 = &uStack_2c;
        }
      }
      else {
        uVar13 = (uint)&uStack_25 ^ 0x2f4b32c9;
        uVar16 = uVar13 + 0x316c04c5;
        uVar11 = (uint)&uStack_25 ^ 0x2f4b32c9;
        uVar12 = uVar11 + 0x316c04c5;
        uVar9 = 0xcd1d41d9;
        if (((uVar2 ^ (uint)&uStack_56 ^ 0x13247) * 0xe331 & 0x10000) == 0) {
          uVar9 = 0xb504eade;
        }
        if ((uVar16 ^ uVar13) * 0x316c04c5 + uVar16 != (uVar12 ^ uVar11) * 0x316c04c5 + uVar12 + 1)
        {
          puVar6 = &uStack_2c;
        }
      }
    }
    else if (uVar9 == 1) {
      uVar9 = (uint)&uStack_25 ^ 0x7eabc09b;
      uVar11 = (uint)&uStack_25 ^ 0x7eabc09b;
      puVar14 = &uStack_2c;
      if ((uVar9 * 0x55ca1380 ^ uVar9 * 0xcab9427 >> 0xd) ==
          (uVar11 * 0x55ca1380 ^ uVar11 * 0xcab9427 >> 0xd) + 1) {
        puVar14 = local_34;
      }
      uVar9 = (*puVar14 ^ 0xa759b4d0) * 0x1fd7e7af + 0x97b3f3e2;
      uVar9 = uVar9 >> 0x1e | uVar9 * 4;
      if ((int)uVar9 < 0x2697d0f0) {
        if (uVar9 == 0xc748c1d4) {
          uVar11 = uVar1 + 0x4919e8b0 ^ 0xa2dc7091;
          uVar12 = uVar1 + 0x4919e8b0 ^ 0xa2dc7091;
          uVar9 = 0xe0a09b98;
          if (((uVar2 ^ (uint)&uStack_5a ^ 0x38993029) * 0xc50c280 & 0x20000000) == 0) {
            uVar9 = 0xbc5e7462;
          }
          if ((uVar12 * 0x2cc10800 | uVar12 * -0x143a67df >> 0x15) !=
              uVar11 * 0x2cc10800 + (uVar11 * -0x143a67df >> 0x15) + 1) {
            puVar6 = &uStack_2c;
          }
        }
        else {
          if (uVar9 != 0xdfd39598) {
            return local_8c;
          }
          uVar12 = (uint)&uStack_25 ^ 0xcda72586;
          uVar11 = (uint)&uStack_25 ^ 0xcda72586;
          uVar9 = 0x144f9678;
          if (*local_78 == 0) {
            uVar9 = 0x9ccd3a8d;
          }
          if ((uVar11 * -0x4d56cc80 ^ uVar11 * -0x1c9aad99 >> 0xd) !=
              (uVar12 * -0x4d56cc80 ^ uVar12 * -0x1c9aad99 >> 0xd) + 1) {
            puVar6 = &uStack_2c;
          }
        }
      }
      else {
        if (uVar9 != 0x2697d0f0) {
          uVar11 = (uint)&uStack_25 ^ 0xbabd16d5;
          uVar9 = 0xbc5e7462;
          uVar12 = (uint)&uStack_25 ^ 0xbabd16d5;
          uVar16 = uVar11 * -0x12239fb1;
          uVar13 = uVar12 * -0x12239fb1;
          uVar11 = uVar11 * -0x11cfd880;
          uVar12 = uVar12 * -0x11cfd880;
          goto LAB_000111d0;
        }
        local_70 = local_70 + 1;
        uVar9 = 0xd896e14e;
        if (local_70 < local_84) {
          uVar9 = 0xf0b55516;
        }
        uVar11 = uVar1 + 0xaf2b66ab ^ 0x30046758;
        uVar12 = uVar1 + 0xaf2b66ab ^ 0x30046758;
        uVar12 = uVar12 * 0x780f9800 | uVar12 * -0x60d0fe0d >> 0x15;
        iVar4 = uVar11 * 0x780f9800 + (uVar11 * -0x60d0fe0d >> 0x15);
LAB_00010b00:
        bVar17 = uVar12 == iVar4 + 1U;
LAB_00010b08:
        if (!bVar17) {
          puVar6 = &uStack_2c;
        }
      }
    }
    else {
      uVar9 = uVar1 + 0x10c0f889 ^ 0x93ed735b;
      uVar11 = uVar1 + 0x10c0f889 ^ 0x93ed735b;
      puVar14 = &uStack_2c;
      if ((uVar9 * 0x6c5e9800 | uVar9 * -0x7cd2742d >> 0x15) ==
          uVar11 * 0x6c5e9800 + (uVar11 * -0x7cd2742d >> 0x15) + 1) {
        puVar14 = local_34;
      }
      uVar9 = (*puVar14 ^ 0x3b00a512) * 0x780e7f1f + 0x3b7054dc;
      if ((uVar9 >> 0x1a | uVar9 * 0x40) == 0x16088291) {
        uVar11 = (uint)&uStack_25 ^ 0x2c3b2fb4;
        uVar9 = 0x5fa9f76c;
        uVar12 = (uint)&uStack_25 ^ 0x2c3b2fb4;
        uVar16 = uVar11 * -0x6560600b;
        uVar13 = uVar12 * -0x6560600b;
        uVar11 = uVar11 * 0x4fcffa80;
        uVar12 = uVar12 * 0x4fcffa80;
LAB_000111d0:
        uVar11 = uVar11 ^ uVar16 >> 0xd;
        uVar12 = uVar12 ^ uVar13 >> 0xd;
LAB_000111dc:
        bVar17 = uVar11 == uVar12 + 1;
        goto LAB_00010b08;
      }
      if ((uVar9 >> 0x1a | uVar9 * 0x40) == 0x66b74adf) {
        local_6c = local_6c + 1;
        uVar16 = (uint)&uStack_25 ^ 0x71fa1d33;
        uVar11 = uVar16 + 0x3c87a32f;
        uVar12 = (uint)&uStack_25 ^ 0x71fa1d33;
        uVar13 = uVar12 + 0x3c87a32f;
        uVar9 = 0x934c80ad;
        if (local_6c < local_80) {
          uVar9 = 0x13d3e5c3;
        }
        if ((uVar11 ^ uVar16) * 0x3c87a32f + uVar11 != (uVar13 ^ uVar12) * 0x3c87a32f + uVar13 + 1)
        {
          puVar6 = &uStack_2c;
        }
      }
      else {
        uVar9 = 0x9c0a9893;
        uVar11 = uVar1 + 0xd1539f68 ^ 0x7082d336;
        uVar12 = uVar1 + 0xd1539f68 ^ 0x7082d336;
        if ((uVar12 * -0x759d0800 | uVar12 * -0x5e2eb3a1 >> 0x15) !=
            uVar11 * -0x759d0800 + (uVar11 * -0x5e2eb3a1 >> 0x15) + 1) {
          puVar6 = &uStack_2c;
        }
        local_74 = 0;
        local_7c = ((uint)&uStack_57 & 3) + 1;
      }
    }
    *puVar6 = uVar9;
  } while( true );
}

