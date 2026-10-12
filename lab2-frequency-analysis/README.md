# Laboratory Work No. 2 – Cryptanalysis of Monoalphabetic Ciphers

**Author:** Macari Chiril-Adam, FAF-243 · **Variant:** 15

An English text encrypted with a monoalphabetic substitution cipher was broken by **frequency analysis**, using the online tool [Frequency Analysis: Breaking the Code](https://crypto.interactive-maths.com/frequency-analysis-breaking-the-code.html) (Crypto Corner). Only letters were encrypted; spaces, digits and punctuation were left unchanged.

| File | Contents |
|---|---|
| [`ciphertext_v15.txt`](ciphertext_v15.txt) | The intercepted cryptogram (variant 15) |
| [`plaintext_v15.txt`](plaintext_v15.txt) | The recovered message |
| [`report/`](report/) | Report with the full step-by-step attack and screenshots |

## Steps of the attack

| Step | Substitutions (cipher → plain) | Reason |
|---|---|---|
| 1 | V → e, W → t | The two most frequent cipher letters (13.8%, 8.9%) match E and T |
| 2 | Q → h, T → a | `tQe` → "the" (the most common word); `thTt` → "that" |
| 3 | X → i, P → s, G → n | Two-letter words `Xt`, `XP`, `XG` → "it", "is", "in" |
| 4 | N → o, O → d | `tN` → "to"; `anO` → "and" |
| 5 | I → r, S → l, J → g, U → p, H → c, F → y | `theiI` → "their"; title `teSeJraUh` → "telegraph"; `HryptograUhF` → "cryptography" |
| 6 | Z → m, D → u, C → f, R → w, A → b | "made", "Samuel", "for", "what", "published" |
| 7 | K → v, L → k, Y → x, M → z, B → q, E → j | "vocabulary", "key", "next", "dozens", "equal", "just" |

## Recovered key

```
Plain:  a b c d e f g h i j k l m n o p q r s t u v w x y z
Cipher: T A H O V C J Q X E L S Z G N U B I P W D K R Y F M
```

The plaintext is an excerpt about the telegraph and its influence on cryptography; it begins *"The telegraph made cryptography what it is today."*
