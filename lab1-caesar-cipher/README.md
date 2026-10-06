# Laboratory Work No. 1 – Caesar Cipher

**Author:** Macari Chiril-Adam, FAF-243

Two Python programs, each with a simple Tkinter GUI, that implement the Caesar cipher over the 31-letter Romanian alphabet:

| File | Task |
|---|---|
| `caesar_task1.py` | Task 1.1: classic Caesar cipher, key `k ∈ {1, …, 30}` |
| `caesar_task2.py` | Task 1.2: Caesar cipher with two keys (shift + keyword permutation of the alphabet) |

Letter encoding (Table 2): `A=0, Ă=1, Â=2, B=3, …, Ș=22, T=23, Ț=24, …, Z=30`.
The shift is computed only with these codes, never with ASCII or Unicode code points.

* Encryption: `c = (x + k) mod 31`
* Decryption: `m = (y − k) mod 31`

## Running

Requires Python 3.8+ (Tkinter is included in the standard Windows/macOS installers).

```bash
python caesar_task1.py
python caesar_task2.py
```

## Report

The report is in [`report/`](report/).

## Input rules

* Key 1: an integer from 1 to 30.
* Key 2 (Task 1.2 only): a keyword of at least 7 Romanian letters, with no spaces, digits or symbols.
* Text: Romanian letters (upper or lower case) and spaces. The text is converted to uppercase and the spaces are removed before processing.
* `Ş`/`Ţ` typed with a cedilla are accepted as `Ș`/`Ț`.
* If any input is invalid, the program shows an error message that names the allowed values (and the rejected character), then puts the cursor back in that field.
