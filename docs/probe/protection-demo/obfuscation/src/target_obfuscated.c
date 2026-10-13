#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
__attribute__((noinline,used,annotate("obf: substitution(prob=100,loop=2), bcf(prob=100,loop=1,maxBlocks=200), flattening(minBlocks=2,maxBlocks=200)"))) uint32_t secret_transform(uint32_t x) {
    return ((x ^ 0x5a17u) * 33u + 7u) & 0xffffu;
}
__attribute__((noinline,used,annotate("obf: substitution(prob=100,loop=2), bcf(prob=100,loop=1,maxBlocks=200), flattening(minBlocks=2,maxBlocks=200)"))) uint32_t simple_checksum(const char *s) {
    uint32_t sum = 0;
    while (*s) sum = (sum * 31u + (unsigned char)*s++) & 0xffffu;
    return sum;
}
int main(int argc, char **argv) {
    const char *marker = "LICENSE_KEY_CHECK_V1";
    uint32_t x = argc > 1 ? (uint32_t)strtoul(argv[1], 0, 10) : 1234u;
    printf("%s %u %u\n", marker, secret_transform(x), simple_checksum(marker));
    return 0;
}
