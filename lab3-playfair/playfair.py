"""
Laboratory Work No. 3 - Task 3.1
Playfair cipher for the Romanian alphabet, with a simple Tkinter GUI.

The Romanian alphabet has 31 letters, but a 5 x 6 matrix has only 30 cells,
so the letter Â is merged into Î (they denote the same sound); after
decryption Â is restored by hand, just like J is restored from I in the
classic English Playfair.

Author: Macari Chiril-Adam, FAF-243
"""

import tkinter as tk
import unicodedata
from tkinter import messagebox

# ---------------------------------------------------------------------------
# 1. Alphabet and matrix size
# ---------------------------------------------------------------------------
ROMANIAN_ALPHABET = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"   # 31 letters (input)
MATRIX_ALPHABET = "AĂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"     # 30 letters (Â -> Î)
ROWS, COLS = 5, 6

MERGE = {"Â": "Î"}                                   # letter merged to fit 30 cells
CEDILLA_FIX = {"Ş": "Ș", "ş": "ș", "Ţ": "Ț", "ţ": "ț"}
ALLOWED_LETTERS = set(ROMANIAN_ALPHABET) | set(ROMANIAN_ALPHABET.lower())
SPACES = {" ", "\n", "\t", "\r"}

FILLER = "X"            # inserted between doubled letters / at the end
ALT_FILLER = "Q"        # used when the letter itself is X
KEY_MIN_LEN = 7

assert len(MATRIX_ALPHABET) == ROWS * COLS


# ---------------------------------------------------------------------------
# 2. Input validation and normalization
# ---------------------------------------------------------------------------
def normalize(raw, what):
    """Check that `raw` has only Romanian letters (and spaces), then return it
    in uppercase, without spaces, with Ş/Ţ fixed and Â merged into Î."""
    text = unicodedata.normalize("NFC", raw)
    text = "".join(CEDILLA_FIX.get(ch, ch) for ch in text)
    for position, ch in enumerate(text, start=1):
        if ch in SPACES:
            continue
        if ch not in ALLOWED_LETTERS:
            shown = repr(ch) if ch.strip() else "a whitespace character"
            raise ValueError(
                f"Invalid character {shown} at position {position} of the {what}.\n\n"
                "Allowed characters: the letters 'A'-'Z' and 'a'-'z' together with "
                "Ă, Â, Î, Ș, Ț (uppercase or lowercase). Spaces are ignored; digits, "
                "punctuation and other symbols are not allowed."
            )
    letters = "".join(ch for ch in text if ch not in SPACES).upper()
    return "".join(MERGE.get(ch, ch) for ch in letters)


def validate_key(raw):
    key = normalize(raw, "key")
    if len(key) < KEY_MIN_LEN:
        raise ValueError(
            f"The key is too short: {len(key)} letter(s).\n\n"
            f"The key must contain at least {KEY_MIN_LEN} letters of the Romanian alphabet."
        )
    return key


def validate_text(raw, what="message"):
    text = normalize(raw, what)
    if not text:
        raise ValueError(f"The {what} is empty.\n\nEnter at least one Romanian letter.")
    return text


# ---------------------------------------------------------------------------
# 3. Building the encryption matrix
# ---------------------------------------------------------------------------
def remove_duplicates(key):
    """Keep only the first occurrence of each letter (e.g. DUBLURA -> DUBLRA)."""
    result = []
    for letter in key:
        if letter not in result:
            result.append(letter)
    return "".join(result)


def build_matrix(key):
    """Fill the 5 x 6 matrix row by row: key letters first, then the remaining
    letters of the alphabet in their natural order."""
    order = remove_duplicates(key + MATRIX_ALPHABET)
    matrix = [list(order[r * COLS:(r + 1) * COLS]) for r in range(ROWS)]
    position = {matrix[r][c]: (r, c) for r in range(ROWS) for c in range(COLS)}
    return matrix, position


# ---------------------------------------------------------------------------
# 4. Preparing the message: split into pairs
# ---------------------------------------------------------------------------
def filler_for(letter):
    return ALT_FILLER if letter == FILLER else FILLER


def make_pairs(text):
    """Split the text into pairs of letters. A filler is inserted between two
    identical letters of the same pair, and added at the end if the number of
    letters is odd."""
    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else None
        if b is None:                      # last letter alone -> add filler
            pairs.append(a + filler_for(a))
            i += 1
        elif a == b:                       # double letter -> insert filler
            pairs.append(a + filler_for(a))
            i += 1
        else:
            pairs.append(a + b)
            i += 2
    return pairs


def split_ciphertext(text):
    """Ciphertext must already consist of valid pairs."""
    if len(text) % 2 != 0:
        raise ValueError(
            f"The ciphertext has an odd number of letters ({len(text)}).\n\n"
            "A Playfair ciphertext always has an even number of letters."
        )
    pairs = [text[i:i + 2] for i in range(0, len(text), 2)]
    for n, pair in enumerate(pairs, start=1):
        if pair[0] == pair[1]:
            raise ValueError(
                f"Pair {n} ('{pair}') contains two identical letters.\n\n"
                "Such a pair can never appear in a Playfair ciphertext."
            )
    return pairs


# ---------------------------------------------------------------------------
# 5. Encryption and decryption of one pair (the three Playfair rules)
# ---------------------------------------------------------------------------
def transform_pair(pair, matrix, position, direction):
    """direction = +1 for encryption, -1 for decryption."""
    (r1, c1), (r2, c2) = position[pair[0]], position[pair[1]]
    if r1 == r2:                                   # rule 2: same row
        return (matrix[r1][(c1 + direction) % COLS] +
                matrix[r2][(c2 + direction) % COLS])
    if c1 == c2:                                   # rule 3: same column
        return (matrix[(r1 + direction) % ROWS][c1] +
                matrix[(r2 + direction) % ROWS][c2])
    return matrix[r1][c2] + matrix[r2][c1]         # rule 1: rectangle


def encrypt(message, key):
    matrix, position = build_matrix(key)
    pairs = make_pairs(message)
    return pairs, [transform_pair(p, matrix, position, +1) for p in pairs]


def decrypt(ciphertext, key):
    matrix, position = build_matrix(key)
    pairs = split_ciphertext(ciphertext)
    return pairs, [transform_pair(p, matrix, position, -1) for p in pairs]


# ---------------------------------------------------------------------------
# 6. GUI
# ---------------------------------------------------------------------------
BG = "#f4f5f7"
CARD = "#ffffff"
ACCENT = "#0f7a5c"
ERROR = "#c62828"
FONT = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
MONO = ("Consolas", 11)


class PlayfairApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lab 3 - Task 3.1 - Playfair Cipher (Romanian alphabet)")
        self.configure(bg=BG, padx=16, pady=14)
        self.resizable(False, False)

        self.operation = tk.StringVar(value="encrypt")
        self.status = tk.StringVar(value="Choose an operation, enter the key and the text.")

        tk.Label(self, text="Playfair Cipher - Romanian alphabet (5 × 6 matrix, Â = Î)",
                 font=("Segoe UI", 14, "bold"), bg=BG, fg=ACCENT).grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

        # Operation
        tk.Label(self, text="Operation:", font=FONT_BOLD, bg=BG).grid(row=1, column=0, sticky="w")
        ops = tk.Frame(self, bg=BG)
        ops.grid(row=1, column=1, sticky="w")
        for text, value in (("Encrypt", "encrypt"), ("Decrypt", "decrypt")):
            tk.Radiobutton(ops, text=text, value=value, variable=self.operation, font=FONT,
                           bg=BG, activebackground=BG, highlightthickness=0,
                           command=self._update_labels).pack(side="left", padx=(0, 12))

        # Key
        tk.Label(self, text="Key (min 7 letters):", font=FONT_BOLD, bg=BG).grid(
            row=2, column=0, sticky="w", pady=6, padx=(0, 10))
        self.key_entry = tk.Entry(self, width=34, font=MONO, relief="solid", bd=1)
        self.key_entry.grid(row=2, column=1, sticky="w", pady=6)
        self.key_entry.bind("<KeyRelease>", lambda _e: self._preview_matrix())

        # Input text
        self.input_label = tk.Label(self, text="Message:", font=FONT_BOLD, bg=BG)
        self.input_label.grid(row=3, column=0, sticky="nw", pady=(4, 0))
        self.input_text = tk.Text(self, width=52, height=4, font=MONO, wrap="word",
                                  relief="solid", bd=1)
        self.input_text.grid(row=3, column=1, sticky="w", pady=(4, 0))

        # Buttons
        buttons = tk.Frame(self, bg=BG)
        buttons.grid(row=4, column=1, sticky="w", pady=10)
        self.run_button = tk.Button(buttons, text="Encrypt", width=12, font=FONT_BOLD, bg=ACCENT,
                                    fg="white", activebackground="#0b5e47",
                                    activeforeground="white", relief="flat", command=self.run)
        self.run_button.pack(side="left")
        tk.Button(buttons, text="Use result as input", font=FONT, relief="groove",
                  command=self.result_to_input).pack(side="left", padx=8)
        tk.Button(buttons, text="Clear", font=FONT, relief="groove",
                  command=self.clear).pack(side="left")

        # Pairs and result
        tk.Label(self, text="Pairs:", font=FONT_BOLD, bg=BG).grid(row=5, column=0, sticky="nw")
        self.pairs_text = self._readonly_text(row=5, height=3)
        tk.Label(self, text="Result (pairs):", font=FONT_BOLD, bg=BG).grid(
            row=6, column=0, sticky="nw", pady=(6, 0))
        self.result_pairs = self._readonly_text(row=6, height=3, pady=(6, 0))
        tk.Label(self, text="Result:", font=FONT_BOLD, bg=BG).grid(
            row=7, column=0, sticky="nw", pady=(6, 0))
        self.result_text = self._readonly_text(row=7, height=3, pady=(6, 0), bg="#e8f4ef")

        # Matrix (right side)
        side = tk.Frame(self, bg=BG)
        side.grid(row=1, column=2, rowspan=7, sticky="n", padx=(18, 0))
        tk.Label(side, text="Encryption matrix (5 × 6)", font=FONT_BOLD, bg=BG).pack(anchor="w")
        self.matrix_frame = tk.Frame(side, bg=CARD, highlightbackground="#c9ced6",
                                     highlightthickness=1)
        self.matrix_frame.pack(anchor="w", pady=(4, 0))
        self.key_info = tk.StringVar(value="Key without repeated letters: -")
        tk.Label(side, textvariable=self.key_info, font=FONT, bg=BG, fg="#555555",
                 wraplength=260, justify="left").pack(anchor="w", pady=(6, 0))
        tk.Label(side, text=f"Filler letter: {FILLER} ({ALT_FILLER} after {FILLER})\n"
                            "Â is written as Î",
                 font=FONT, bg=BG, fg="#555555", justify="left").pack(anchor="w", pady=(4, 0))
        self._show_matrix(None)

        # Status line
        self.status_label = tk.Label(self, textvariable=self.status, font=FONT, bg=BG,
                                     fg="#555555", anchor="w", justify="left", wraplength=820)
        self.status_label.grid(row=8, column=0, columnspan=3, sticky="we", pady=(10, 0))

        self.bind("<Control-Return>", lambda _e: self.run())
        self.key_entry.focus_set()

    # --- helpers ----------------------------------------------------------
    def _readonly_text(self, row, height, pady=0, bg="#f9fafb"):
        widget = tk.Text(self, width=52, height=height, font=MONO, wrap="word",
                         relief="solid", bd=1, bg=bg, state="disabled")
        widget.grid(row=row, column=1, sticky="w", pady=pady)
        return widget

    def _set(self, widget, text):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.config(state="disabled")

    def _show_matrix(self, matrix, key_len=0):
        for child in self.matrix_frame.winfo_children():
            child.destroy()
        for r in range(ROWS):
            for c in range(COLS):
                letter = matrix[r][c] if matrix else "·"
                in_key = matrix and r * COLS + c < key_len
                tk.Label(self.matrix_frame, text=letter, width=3, height=1,
                         font=("Consolas", 14, "bold"),
                         bg="#d7efe6" if in_key else CARD,
                         relief="ridge", bd=1).grid(row=r, column=c)

    def _preview_matrix(self):
        try:
            key = validate_key(self.key_entry.get())
        except ValueError:
            self._show_matrix(None)
            self.key_info.set("Key without repeated letters: -")
            return
        matrix, _ = build_matrix(key)
        unique = remove_duplicates(key)
        self._show_matrix(matrix, len(unique))
        self.key_info.set(f"Key without repeated letters: {unique}")

    def _update_labels(self):
        is_encrypt = self.operation.get() == "encrypt"
        self.run_button.config(text="Encrypt" if is_encrypt else "Decrypt")
        self.input_label.config(text="Message:" if is_encrypt else "Ciphertext:")

    def _error(self, title, message, widget):
        self.status.set(message.split("\n")[0])
        self.status_label.config(fg=ERROR)
        messagebox.showerror(title, message, parent=self)
        widget.focus_set()
        if isinstance(widget, tk.Entry):
            widget.select_range(0, "end")
        else:
            widget.tag_add("sel", "1.0", "end-1c")

    # --- actions ----------------------------------------------------------
    def run(self):
        for w in (self.pairs_text, self.result_pairs, self.result_text):
            self._set(w, "")
        try:
            key = validate_key(self.key_entry.get())
        except ValueError as e:
            self._error("Invalid key", str(e), self.key_entry)
            return
        is_encrypt = self.operation.get() == "encrypt"
        what = "message" if is_encrypt else "ciphertext"
        try:
            text = validate_text(self.input_text.get("1.0", "end-1c"), what)
            pairs, result = encrypt(text, key) if is_encrypt else decrypt(text, key)
        except ValueError as e:
            self._error(f"Invalid {what}", str(e), self.input_text)
            return

        self._preview_matrix()
        self._set(self.pairs_text, " ".join(pairs))
        self._set(self.result_pairs, " ".join(result))
        self._set(self.result_text, "".join(result))
        if is_encrypt:
            self.status.set(f"Encrypted {len(pairs)} pairs. Fillers ({FILLER}/{ALT_FILLER}) were "
                            "inserted between doubled letters and at the end if needed.")
        else:
            self.status.set(f"Decrypted {len(pairs)} pairs. Remove the filler letters and add "
                            "spaces (and Â instead of Î where needed) manually.")
        self.status_label.config(fg="#2e7d32")

    def result_to_input(self):
        result = self.result_text.get("1.0", "end-1c")
        if not result:
            return
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", result)
        self.operation.set("decrypt" if self.operation.get() == "encrypt" else "encrypt")
        self._update_labels()
        for w in (self.pairs_text, self.result_pairs, self.result_text):
            self._set(w, "")

    def clear(self):
        self.key_entry.delete(0, "end")
        self.input_text.delete("1.0", "end")
        for w in (self.pairs_text, self.result_pairs, self.result_text):
            self._set(w, "")
        self._show_matrix(None)
        self.key_info.set("Key without repeated letters: -")
        self.status.set("Choose an operation, enter the key and the text.")
        self.status_label.config(fg="#555555")
        self.key_entry.focus_set()


if __name__ == "__main__":
    PlayfairApp().mainloop()
