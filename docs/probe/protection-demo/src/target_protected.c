#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
__attribute__((noinline,used)) static uint32_t secret_transform(uint32_t x) {
    return ((x ^ 0x5a17u) * 33u + 7u) & 0xffffu;
}
__attribute__((noinline,used)) static uint32_t simple_checksum(const char *s) {
    uint32_t sum = 0;
    while (*s) sum = (sum * 31u + (unsigned char)*s++) & 0xffffu;
    return sum;
}
int main(int argc, char **argv) {
    /* Fixed XOR encoding hides the static string, not a cryptographic secret.
       Volatile reads prevent -O2 from folding the decoder into plaintext. */
    static const unsigned char encoded_marker[] = { 0xeb, 0xee, 0xe4, 0xe2, 0xe9, 0xf4, 0xe2, 0xf8, 0xec, 0xe2, 0xfe, 0xf8, 0xe4, 0xef, 0xe2, 0xe4, 0xec, 0xf8, 0xf1, 0x96 };
    const volatile unsigned char *encoded = encoded_marker;
    char marker[sizeof(encoded_marker) + 1];
    for (size_t i = 0; i < sizeof(encoded_marker); ++i)
        marker[i] = (char)(encoded[i] ^ 0xa7u);
    marker[sizeof(encoded_marker)] = '\0';
    uint32_t x = argc > 1 ? (uint32_t)strtoul(argv[1], 0, 10) : 1234u;
    printf("%s %u %u\n", marker, secret_transform(x), simple_checksum(marker));
    return 0;
}
