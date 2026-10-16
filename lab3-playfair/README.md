# Laboratory Work No. 3 – Polyalphabetic Ciphers: Playfair (Task 3.1)

**Author:** Macari Chiril-Adam, FAF-243

`playfair.py` implements the Playfair cipher for the 31-letter Romanian alphabet, with a simple Tkinter GUI.

## Running

```bash
python playfair.py
```

Requires Python 3.8+ (Tkinter is included in the standard Windows/macOS installers).

## How the algorithm is adapted to Romanian

* **Matrix 5 × 6 (30 cells).** The alphabet has 31 letters, so **Â is merged into Î** (they are the same sound, like I/J in the English Playfair). After decryption, Â is restored manually.
* Matrix alphabet: `A Ă B C D E F G H I Î J K L M N O P Q R S Ș T Ț U V W X Y Z`
* **Filler letter:** `X` goes between doubled letters of a pair and at the end of an odd-length text. If the letter itself is `X`, the filler is `Q`.
* The key loses its repeated letters (e.g. `SECURITATE` → `SECURITA`), is written row by row, and the rest of the alphabet follows.
* Rules: **rectangle** → swap columns; **same row** → letter to the right (left when decrypting); **same column** → letter below (above when decrypting).

## Input rules

* Only letters `A–Z`, `a–z` and `Ă Â Î Ș Ț` (Ş/Ţ with a cedilla are accepted too). Spaces are ignored. For any other character, the program names it and suggests the allowed range.
* The key must have at least 7 letters.
* A ciphertext must have an even number of letters, and no pair may contain two identical letters.
* As the task requires, removing fillers and adding spaces after decryption is done manually.

## Example

Key `Securitate`, message `Copiii merg la școală mâine dimineață`:

```
Pairs:      CO PI IX IM ER GL AȘ CO AL ĂM ÎI NE DI MI NE AȚ ĂX
Ciphertext: ĂW ȘU UZ SȘ CI HG FN ĂW FH TO LC VA FR ȘS VA TV BW
```
