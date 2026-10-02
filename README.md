# vanity-difficulty

Estimates how many keys, and how much time, a vanity address search needs for a given prefix.
Supports EVM, Solana and Bitcoin addresses.

```bash
python vanity.py 0xdead --rate 50000000
python vanity.py 0xDeAd --rate 50000000 --case-sensitive   # EIP-55 mixed case
python vanity.py sol:Moon --rate 2000000
python vanity.py btc:1Kid --rate 5000000
```

```
pattern      0xdead (evm, 4 chars, case-insensitive)
difficulty   1 in 65,536
50% chance   45,426 keys -> 0.00s at 50,000,000 keys/s
90% chance   150,901 keys -> 0.00s at 50,000,000 keys/s
99% chance   301,802 keys -> 0.01s at 50,000,000 keys/s
```

How the numbers are computed:

- EVM (hex): each character has 16 possibilities. With `--case-sensitive`, every letter also has to
  match its EIP-55 case, which halves the odds per letter.
- Solana and Bitcoin (base58): each character has 58 possibilities and case is part of the alphabet.
- Bitcoin legacy addresses always start with `1`, so that character is free.
- The chance of success after `n` keys is `1 - (1 - 1/d)^n`.

In practice base58 prefixes are not uniform, because the leading characters depend on the size of
the number. The Solana and Bitcoin figures are good for the order of magnitude only.

## Tests

```bash
python -m unittest -v
```
