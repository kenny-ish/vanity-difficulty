"""Vanity address search time estimator."""
import argparse
import math

HEX = set("0123456789abcdefABCDEF")
B58 = set("123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")


def difficulty(pattern: str, case_sensitive: bool = False) -> tuple[str, int]:
    if pattern.startswith("0x"):
        body = pattern[2:]
        if not body or any(c not in HEX for c in body):
            raise ValueError("EVM prefix must be hex")
        d = 16 ** len(body)
        if case_sensitive:
            d *= 2 ** sum(c.isalpha() for c in body)
        return "evm", d
    chain, _, body = pattern.partition(":")
    if chain not in ("sol", "btc") or not body:
        raise ValueError("use 0x..., sol:PREFIX or btc:1PREFIX")
    if any(c not in B58 for c in body):
        raise ValueError("base58 excludes 0, O, I and l")
    if chain == "btc":
        if not body.startswith("1"):
            raise ValueError("legacy bitcoin addresses start with 1")
        body = body[1:]
    return chain, 58 ** len(body)


def keys_for(prob: float, d: int) -> float:
    if d == 1:
        return 1
    return math.log(1 - prob) / math.log1p(-1 / d)


def fmt_time(secs: float) -> str:
    for unit, size in (("years", 31_557_600), ("days", 86_400), ("h", 3600), ("min", 60)):
        if secs >= size:
            return f"{secs / size:,.1f} {unit}"
    return f"{secs:.2f}s"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pattern")
    ap.add_argument("--rate", type=float, default=1_000_000, help="keys per second")
    ap.add_argument("--case-sensitive", action="store_true")
    a = ap.parse_args()

    chain, d = difficulty(a.pattern, a.case_sensitive)
    body = a.pattern[2:] if chain == "evm" else a.pattern.split(":", 1)[1]
    mode = "case-sensitive" if (a.case_sensitive or chain != "evm") else "case-insensitive"
    print(f"pattern      {a.pattern} ({chain}, {len(body)} chars, {mode})")
    print(f"difficulty   1 in {d:,}")
    for p in (0.5, 0.9, 0.99):
        n = keys_for(p, d)
        print(f"{p:.0%} chance   {n:,.0f} keys -> {fmt_time(n / a.rate)} at {a.rate:,.0f} keys/s")


if __name__ == "__main__":
    main()
