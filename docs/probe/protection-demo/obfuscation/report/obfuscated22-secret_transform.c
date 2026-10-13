
uint secret_transform(uint param_1)

{
  uint uVar1;
  uint uVar2;
  uint uVar3;
  uint uVar4;
  uint uVar5;
  uint uVar6;
  uint uVar7;
  uint uVar8;
  undefined1 auStack_1f [2];
  undefined1 uStack_1d;
  undefined1 uStack_1c;
  undefined1 uStack_1b;
  undefined1 uStack_1a;
  undefined1 uStack_19;
  
  uVar1 = (uint)&uStack_1d ^ 0x4adfbbb3;
  uVar4 = (uint)&uStack_1d ^ 0xb520444c;
  uVar4 = (uVar4 & ~(uint)auStack_1f | uVar1 & (uint)auStack_1f) ^
          (uVar4 & 0x7775ad60 | uVar1 & 0x888a529f);
  uVar1 = (uint)&uStack_1c ^ 0x243f75f4;
  uVar5 = ((((uint)&uStack_1c ^ 0xdbc08a0b) & ~param_1 | uVar1 & param_1) ^ uVar1) & uVar4;
  uVar6 = (uint)&uStack_1b ^ 0x2c2203e8;
  uVar8 = (uint)&uStack_1b ^ 0xd3ddfc17;
  param_1 = param_1 & ~uVar4;
  uVar2 = ~uVar4 | 0x5a17;
  uVar1 = (uint)&uStack_1a ^ 0xee3f71d;
  uVar7 = (uint)&uStack_1a ^ 0xf11c08e2;
  uVar3 = uVar4 & 0x5a17 ^ 0xffffa5e8;
  uVar1 = (((uVar8 & ~param_1 | param_1 & uVar6) ^ (uVar8 & ~uVar5 | uVar5 & uVar6) |
           param_1 & uVar5) ^
          ((uVar3 & uVar1 | (uVar4 & 0x5a17 ^ 0x5a17) & uVar7) ^ (uVar2 & uVar1 | uVar7 & ~uVar2) |
          ~(uVar3 | uVar2))) * 0x21 + 7;
  uVar2 = (uint)&uStack_19 ^ 0xaf4cc582;
  uVar4 = (uint)&uStack_19 ^ 0x50b33a7d;
  return ((uVar1 & uVar4 | uVar2 & ~uVar1) ^ (uVar4 & 0xffff) + (uVar2 & 0xffff0000) |
         ~uVar1 & 0xffff0000) ^ 0xffffffff;
}

