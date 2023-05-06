LOG2_LUT = [
    -1, 0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3,
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7
]

SIXTEENP2 = 65536


def to_binary(decimal: int) -> list[int]:
    dec = type(
        "Decimal", (),
        {
            "num": [decimal],
            "rems": [],
            "__call__": lambda self: list(map(lambda x: x(), [lambda self=self: self.rems.append(self.num[0] & 1), lambda self=self: self.num.__setitem__(0, self.num[0] // 2)])),
            "__invert__": lambda self: self.num[0] > 0
        }
    )()

    while ~dec:
        dec()
    dec.rems.reverse()
    return dec.rems


def fast_expontentiation(num: int, exp: int) -> int:
    binary = to_binary(exp)
    final_exp = num
    for b in binary[1:]:
        final_exp *= final_exp
        if b == 1:
            final_exp *= num
    return final_exp


def log2n(num: int) -> int:
    return 24 + LOG2_LUT[num >> 24] if num >> 24 else 16 + LOG2_LUT[num >> 16] if num >> 16 else 8 + LOG2_LUT[num >> 8] if num >> 8 else LOG2_LUT[num]


def precompute_magic_single(divisor: int) -> int:
    if divisor == 0: return 0
    l = log2n(divisor) + 1
    m = (SIXTEENP2 * (fast_expontentiation(2, l) - divisor) // divisor) + 1
    sh1 = 1 if l > 0 else l
    sh2 = l - sh1
    return ((sh1 & 0b1111) | ((sh2 & 0b1111) << 4) | ((m & 0xffffff) << 8)) & 0xffffffff


def test_fast_division(num: int, divisor: int):
    magics = precompute_magic_single(divisor)
    sh1 = magics & 0b1111
    sh2 = (magics >> 4) & 0b1111
    m = (magics >> 8) & 0xffffff
    t1 = (((m * num) >> 16) & 0xffff)
    q = (t1 + ((num - t1) >> sh1)) >> sh2
    print(num // divisor, q, (m, sh1, sh2))


def generate_magic_range(range=range(0, 2000)) -> list[int]:
    return [precompute_magic_single(i) for i in range]


def format_magic_range(rng: list[int], split=8, prefix=".int", pad="08x") -> list[int]:
    rng = list(map(lambda i: '0x' + format(i, pad), rng))
    portions = [rng[i:i+split] for i in range(0, len(rng), split)]
    portions_joined = list(map(", ".join, portions))
    portions_formatted = list(map(lambda p: f"{prefix} {p}", portions_joined))
    return "\n".join(portions_formatted)


if __name__ == "__main__":
    from sys import argv, executable

    def parse_or_default(arg: str, patt: list[str], default: any, fn=int):
        return fn(arg.split("=")[-1]) if any([arg.startswith(s) for s in patt]) else default

    def print_and_exit(_, msg=f"{executable.split('/')[-1]} {argv[0]} [--start/-s]=[0] [--end/-e]=[1000] [--start/-s]=[magics.S] [--sectname/-sn]=[.section magics, \"a\", @progbits] [--perline/-pl]=[2] [--prefix/-pr]=[.int] [--pad/-pd]=[08x]"):
        print(msg)
        exit(1)

    def test_and_exit(exp: str):
        dividend = int(exp.split("/")[0])
        divisor = int(exp.split("/")[1])
        test_fast_division(dividend, divisor)
        exit(0)

    for arg in argv:
        start = parse_or_default(arg, ["--start", "-s"], 0)
        end = parse_or_default(arg, ["--end", "-e"], 1000)
        outp = parse_or_default(arg, ["--out", "-o"], "divmagics.inc", str)
        pad = parse_or_default(arg, ["--pad", "-pd"], "08x", str)
        sectname = parse_or_default(
            arg, ["--sectname", "-sn"], '.section magics, "a", @progbits', str)
        prefix = parse_or_default(arg, ["--prefix", "-pr"], '.int', str)
        perline = parse_or_default(arg, ["--perline", "-pl"], 2)
        _ = parse_or_default(
            arg, ["--help", "-h"], None, print_and_exit)
        _ = parse_or_default(arg, ["--test", "-t"], None, test_and_exit)

    rangerpc = generate_magic_range(range(start, end))
    formatted = format_magic_range(
        rangerpc, perline, prefix=prefix, pad=pad)
    with open(outp, "w") as fw:
        fw.write(f'{sectname}\n{formatted}')
