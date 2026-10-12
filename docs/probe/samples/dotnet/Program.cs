using System;
using System.Runtime.CompilerServices;
public static class BareBaseline {
    [MethodImpl(MethodImplOptions.NoInlining)]
    public static uint secret_transform(uint x) => unchecked(((x ^ 0x5a17u) * 33u + 7u) & 0xffffu);
    [MethodImpl(MethodImplOptions.NoInlining)]
    public static uint simple_checksum(string s) {
        uint sum = 0;
        foreach (char c in s) sum = unchecked((sum * 31u + (byte)c) & 0xffffu);
        return sum;
    }
    public static void Main(string[] args) {
        string marker = "LICENSE_KEY_CHECK_V1";
        uint x = args.Length > 0 ? uint.Parse(args[0]) : 1234u;
        Console.WriteLine($"{marker} {secret_transform(x)} {simple_checksum(marker)}");
    }
}
