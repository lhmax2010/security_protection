using System;
using System.Runtime.CompilerServices;

public static class BareBaseline
{
	[MethodImpl(MethodImplOptions.NoInlining)]
	public static uint secret_transform(uint x)
	{
		return ((x ^ 0x5A17) * 33 + 7) & 0xFFFF;
	}

	[MethodImpl(MethodImplOptions.NoInlining)]
	public static uint simple_checksum(string s)
	{
		uint num = 0u;
		foreach (char c in s)
		{
			num = (num * 31 + (byte)c) & 0xFFFF;
		}
		return num;
	}

	public static void Main(string[] args)
	{
		string text = "LICENSE_KEY_CHECK_V1";
		uint x = ((args.Length != 0) ? uint.Parse(args[0]) : 1234u);
		Console.WriteLine($"{text} {secret_transform(x)} {simple_checksum(text)}");
	}
}
You are not using the latest version of the tool, please update.
Latest version is '11.1.0.9782' (yours is '9.1.0.7988')
