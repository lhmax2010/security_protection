import sys

def secret_transform(x):
    return ((x ^ 0x5a17) * 33 + 7) & 0xffff

def simple_checksum(s):
    total = 0
    for b in s.encode('ascii'):
        total = (total * 31 + b) & 0xffff
    return total

if __name__ == '__main__':
    marker = 'LICENSE_KEY_CHECK_V1'
    x = int(sys.argv[1]) if len(sys.argv) > 1 else 1234
    print(marker, secret_transform(x), simple_checksum(marker))
