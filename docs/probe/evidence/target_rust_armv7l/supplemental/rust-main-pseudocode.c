
/* WARNING: Unknown calling convention: __rustcall */
/* target[903e41bac7e1d2cd]::main */

void __rustcall target[903e41bac7e1d2cd]::main(void)

{
  byte bVar1;
  byte *pbVar2;
  uint uVar3;
  uint uVar4;
  uint uVar5;
  undefined4 *puVar6;
  undefined1 *puStack_48;
  undefined4 uStack_44;
  undefined4 local_40;
  undefined1 *local_3c;
  code *local_38;
  undefined4 *local_34;
  code *local_30;
  int *local_2c;
  code *local_28;
  int local_24;
  byte *local_20;
  uint local_1c;
  
  puStack_48 = &DAT_00053a38;
  uStack_44 = 0x14;
  std::env::args();
  std::env::next();
  if (local_24 != -1) {
    if (local_24 != 0) {
      __rustc[9d087a5ab36ea756]::__rust_dealloc(local_20,local_24,1);
    }
    std::env::next();
    if (local_24 != -1) {
      uVar3 = 0x4d2;
      uVar4 = uVar3;
      if (local_1c != 0) {
        if (local_1c == 1) {
          bVar1 = *local_20;
          if ((bVar1 == 0x2b) || (bVar1 == 0x2d)) goto LAB_000178d8;
        }
        else {
          bVar1 = *local_20;
        }
        pbVar2 = local_20;
        if (bVar1 == 0x2b) {
          pbVar2 = local_20 + 1;
          local_1c = local_1c - 1;
        }
        if (local_1c < 9) {
          if (local_1c == 0) {
            uVar4 = 0;
          }
          else {
            uVar5 = *pbVar2 - 0x30;
            if (((((uVar5 < 10) && (uVar4 = uVar5, local_1c != 1)) &&
                 (uVar4 = uVar3, pbVar2[1] - 0x30 < 10)) &&
                (((uVar5 = (pbVar2[1] - 0x30) + uVar5 * 10, uVar4 = uVar5, local_1c != 2 &&
                  (uVar4 = uVar3, pbVar2[2] - 0x30 < 10)) &&
                 ((uVar5 = (pbVar2[2] - 0x30) + uVar5 * 10, uVar4 = uVar5, local_1c != 3 &&
                  ((uVar4 = uVar3, pbVar2[3] - 0x30 < 10 &&
                   (uVar5 = (pbVar2[3] - 0x30) + uVar5 * 10, uVar4 = uVar5, local_1c != 4)))))))) &&
               ((uVar4 = uVar3, pbVar2[4] - 0x30 < 10 &&
                (((((uVar5 = (pbVar2[4] - 0x30) + uVar5 * 10, uVar4 = uVar5, local_1c != 5 &&
                    (uVar4 = uVar3, pbVar2[5] - 0x30 < 10)) &&
                   (uVar5 = (pbVar2[5] - 0x30) + uVar5 * 10, uVar4 = uVar5, local_1c != 6)) &&
                  ((uVar4 = uVar3, pbVar2[6] - 0x30 < 10 &&
                   (uVar5 = (pbVar2[6] - 0x30) + uVar5 * 10, uVar4 = uVar5, local_1c != 7)))) &&
                 (uVar4 = uVar3, pbVar2[7] - 0x30 < 10)))))) {
              uVar4 = (pbVar2[7] - 0x30) + uVar5 * 10;
            }
          }
        }
        else {
          uVar4 = 0;
          do {
            uVar3 = (uint)((ulonglong)uVar4 * 10);
            if ((int)((ulonglong)uVar4 * 10 >> 0x20) != 0) {
LAB_000178cc:
              uVar4 = 0x4d2;
              break;
            }
            uVar5 = *pbVar2 - 0x30;
            uVar4 = uVar5 + uVar3;
            if ((9 < uVar5) || (CARRY4(uVar5,uVar3))) goto LAB_000178cc;
            pbVar2 = pbVar2 + 1;
            local_1c = local_1c - 1;
          } while (local_1c != 0);
        }
      }
LAB_000178d8:
      if (local_24 != 0) {
        __rustc[9d087a5ab36ea756]::__rust_dealloc(local_20,local_24,1);
      }
      goto LAB_000178e8;
    }
  }
  uVar4 = 0x4d2;
LAB_000178e8:
  if ((int)local_30 - (int)local_38 != 0) {
    puVar6 = (undefined4 *)((int)local_38 + 4);
    uVar3 = (uint)((int)local_30 - (int)local_38) / 0xc;
    do {
      if (puVar6[-1] != 0) {
        __rustc[9d087a5ab36ea756]::__rust_dealloc(*puVar6,puVar6[-1],1);
      }
      puVar6 = puVar6 + 3;
      uVar3 = uVar3 - 1;
    } while (uVar3 != 0);
  }
  if (local_34 != (undefined4 *)0x0) {
    __rustc[9d087a5ab36ea756]::__rust_dealloc(local_3c,(int)local_34 * 0xc,4);
  }
  local_40 = secret_transform(uVar4);
  local_24 = simple_checksum(&DAT_00053a38,0x14);
  local_38 = <&str_as_core[e08171c23a3acbd2]::fmt::Display>::fmt;
  local_30 = core::fmt::num::imp::fmt;
  local_34 = &local_40;
  local_3c = (undefined1 *)&puStack_48;
  local_2c = &local_24;
  local_28 = local_30;
  std::io::stdio::_print();
  return;
}

