"""
Laboratory Work No. 1 - Task 1.2
Caesar cipher with two keys (numeric shift + keyword permutation)
over the Romanian alphabet (n = 31), with a simple Tkinter GUI.

Author: Macari Chiril-Adam, FAF-243
"""

import re
import tkinter as tk
import unicodedata
from tkinter import messagebox

# ---------------------------------------------------------------------------
# 1. Letter encoding (Table 2): A = 0, Ă = 1, Â = 2, ..., Z = 30
# ---------------------------------------------------------------------------
ALPHABET = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"
N = len(ALPHABET)  # 31

CEDILLA_FIX = {"Ş": "Ș", "ş": "ș", "Ţ": "Ț", "ţ": "ț"}
ALLOWED_LETTERS = set(ALPHABET) | set(ALPHABET.lower())
WHITESPACE = {" ", "\n", "\t", "\r"}

KEY_MIN, KEY_MAX = 1, N - 1  # key 1: 1 .. 30
KEYWORD_MIN_LEN = 7          # key 2: at least 7 letters


def mod(a, n):
    """Modulo that always returns a value in 0..n-1, even when a is negative."""
    r = a % n
    if r < 0:
        r += n
    return r


def normalize(raw):
    """NFC-normalize and replace Ş/Ţ (cedilla) with Ș/Ț (comma below)."""
    text = unicodedata.normalize("NFC", raw)
    return "".join(CEDILLA_FIX.get(ch, ch) for ch in text)


# ---------------------------------------------------------------------------
# 2. Input validation
# ---------------------------------------------------------------------------
def validate_key(raw):
    """Key 1: integer from 1 to 30."""
    value = raw.strip()
    if not re.fullmatch(r"[0-9]+", value):
        raise ValueError(
            f"Invalid key 1: '{raw}'.\n\n"
            f"Key 1 must be an integer between {KEY_MIN} and {KEY_MAX} (inclusive)."
        )
    key = int(value)
    if not KEY_MIN <= key <= KEY_MAX:
        raise ValueError(
            f"Invalid key 1: {key} is out of range.\n\n"
            f"Key 1 must be an integer between {KEY_MIN} and {KEY_MAX} (inclusive)."
        )
    return key


def validate_keyword(raw):
    """Key 2: only Romanian letters, length >= 7; returned in uppercase."""
    keyword = normalize(raw.strip())
    for position, ch in enumerate(keyword, start=1):
        if ch not in ALLOWED_LETTERS:
            shown = "space" if ch == " " else f"'{ch}'"
            raise ValueError(
                f"Invalid character {shown} at position {position} of key 2.\n\n"
                "The keyword may contain only letters of the Romanian alphabet "
                "(A-Z, Ă, Â, Î, Ș, Ț), with no spaces, digits or symbols."
            )
    if len(keyword) < KEYWORD_MIN_LEN:
        raise ValueError(
            f"Key 2 is too short: {len(keyword)} letter(s).\n\n"
            f"The keyword must have at least {KEYWORD_MIN_LEN} letters "
            "of the Romanian alphabet."
        )
    return keyword.upper()


def prepare_text(raw):
    """Validate the text, then convert it to uppercase and remove the spaces."""
    text = normalize(raw)
    for position, ch in enumerate(text, start=1):
        if ch in WHITESPACE:
            continue
        if ch not in ALLOWED_LETTERS:
            raise ValueError(
                f"Invalid character '{ch}' at position {position}.\n\n"
                "Allowed: letters of the Romanian alphabet "
                "(A-Z, Ă, Â, Î, Ș, Ț, uppercase or lowercase) and spaces."
            )
    cleaned = "".join(ch for ch in text if ch not in WHITESPACE).upper()
    if not cleaned:
        raise ValueError("The text is empty.\n\nEnter at least one Romanian letter.")
    return cleaned


# ---------------------------------------------------------------------------
# 3. Permuted alphabet: distinct keyword letters first, then the remaining
#    letters of the alphabet in their natural (Table 2) order.
# ---------------------------------------------------------------------------
def build_permuted_alphabet(keyword):
    permuted = []
    for letter in keyword:              # keep only the first occurrence
        if letter not in permuted:
            permuted.append(letter)
    for letter in ALPHABET:             # append the letters not used yet
        if letter not in permuted:
            permuted.append(letter)
    return "".join(permuted)


# ---------------------------------------------------------------------------
# 4. Encryption / decryption using positions in the permuted alphabet
#    c = (x + k1) mod n        m = (y - k1) mod n
# ---------------------------------------------------------------------------
def encrypt(plaintext, k1, permuted):
    position = {letter: i for i, letter in enumerate(permuted)}
    return "".join(permuted[mod(position[letter] + k1, N)] for letter in plaintext)


def decrypt(ciphertext, k1, permuted):
    position = {letter: i for i, letter in enumerate(permuted)}
    return "".join(permuted[mod(position[letter] - k1, N)] for letter in ciphertext)


# ---------------------------------------------------------------------------
# 5. GUI
# ---------------------------------------------------------------------------
BG = "#f4f5f7"
CARD = "#ffffff"
ACCENT = "#6a3fa0"
ERROR = "#c62828"
FONT = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
MONO = ("Consolas", 11)


class CaesarPermutationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lab 1 - Task 1.2 - Caesar Cipher with Permutation (Romanian alphabet)")
        self.configure(bg=BG, padx=16, pady=14)
        self.resizable(False, False)

        self.operation = tk.StringVar(value="encrypt")
        self.status = tk.StringVar(
            value="Choose an operation, enter key 1, key 2 (keyword) and the text.")

        tk.Label(self, text="Caesar Cipher with Permutation - Romanian alphabet (n = 31)",
                 font=("Segoe UI", 14, "bold"), bg=BG, fg=ACCENT).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # Operation
        tk.Label(self, text="Operation:", font=FONT_BOLD, bg=BG).grid(row=1, column=0, sticky="w")
        ops = tk.Frame(self, bg=BG)
        ops.grid(row=1, column=1, sticky="w")
        for text, value in (("Encrypt", "encrypt"), ("Decrypt", "decrypt")):
            tk.Radiobutton(ops, text=text, value=value, variable=self.operation,
                           font=FONT, bg=BG, activebackground=BG, highlightthickness=0,
                           command=self._update_button).pack(side="left", padx=(0, 12))

        # Key 1
        tk.Label(self, text="Key 1 - shift (1-30):", font=FONT_BOLD, bg=BG).grid(
            row=2, column=0, sticky="w", pady=(6, 3))
        self.key_entry = tk.Entry(self, width=8, font=MONO, relief="solid", bd=1)
        self.key_entry.grid(row=2, column=1, sticky="w", pady=(6, 3))

        # Key 2
        tk.Label(self, text="Key 2 - keyword (min 7):", font=FONT_BOLD, bg=BG).grid(
            row=3, column=0, sticky="w", pady=(3, 6), padx=(0, 10))
        self.keyword_entry = tk.Entry(self, width=30, font=MONO, relief="solid", bd=1)
        self.keyword_entry.grid(row=3, column=1, sticky="w", pady=(3, 6))
        self.keyword_entry.bind("<KeyRelease>", lambda _e: self._preview_alphabet())

        # Input text
        self.input_label = tk.Label(self, text="Message:", font=FONT_BOLD, bg=BG)
        self.input_label.grid(row=4, column=0, sticky="nw", pady=(4, 0))
        self.input_text = tk.Text(self, width=62, height=4, font=MONO, wrap="word",
                                  relief="solid", bd=1)
        self.input_text.grid(row=4, column=1, sticky="w", pady=(4, 0))

        # Buttons
        buttons = tk.Frame(self, bg=BG)
        buttons.grid(row=5, column=1, sticky="w", pady=10)
        self.run_button = tk.Button(buttons, text="Encrypt", width=12, font=FONT_BOLD,
                                    bg=ACCENT, fg="white", activebackground="#55318a",
                                    activeforeground="white", relief="flat",
                                    command=self.run)
        self.run_button.pack(side="left")
        tk.Button(buttons, text="Use result as input", font=FONT, relief="groove",
                  command=self.result_to_input).pack(side="left", padx=8)
        tk.Button(buttons, text="Clear", font=FONT, relief="groove",
                  command=self.clear).pack(side="left")

        # Result
        tk.Label(self, text="Result:", font=FONT_BOLD, bg=BG).grid(row=6, column=0, sticky="nw")
        self.output_text = tk.Text(self, width=62, height=4, font=MONO, wrap="char",
                                   relief="solid", bd=1, bg="#f3eefa", state="disabled")
        self.output_text.grid(row=6, column=1, sticky="w")

        # Alphabets: standard (Table 2) and permuted (for checking by hand)
        tk.Label(self, text="Standard alphabet:", font=FONT_BOLD, bg=BG).grid(
            row=7, column=0, sticky="nw", pady=(12, 0))
        self._alphabet_table(ALPHABET).grid(row=7, column=1, sticky="w", pady=(12, 0))

        tk.Label(self, text="Permuted alphabet:", font=FONT_BOLD, bg=BG).grid(
            row=8, column=0, sticky="nw", pady=(8, 0))
        self.permuted_frame = tk.Frame(self, bg=BG)
        self.permuted_frame.grid(row=8, column=1, sticky="w", pady=(8, 0))
        self.permuted_string = tk.StringVar(value="(enter a valid keyword to build it)")
        tk.Label(self, textvariable=self.permuted_string, font=MONO, bg=BG, fg=ACCENT).grid(
            row=9, column=1, sticky="w", pady=(4, 0))
        self._show_permuted(None)

        # Status line
        self.status_label = tk.Label(self, textvariable=self.status, font=FONT, bg=BG,
                                     fg="#555555", anchor="w", justify="left")
        self.status_label.grid(row=10, column=0, columnspan=2, sticky="we", pady=(10, 0))

        self.bind("<Return>", lambda _e: self.run())
        self.key_entry.focus_set()

    # --- helpers ----------------------------------------------------------
    def _alphabet_table(self, letters, parent=None, highlight=0):
        frame = tk.Frame(parent or self, bg=CARD, highlightbackground="#c9ced6",
                         highlightthickness=1)
        for i in range(N):
            letter = letters[i] if letters else "·"
            bg = "#efe7fa" if i < highlight else CARD
            tk.Label(frame, text=letter, font=("Consolas", 9, "bold"), bg=bg, width=2).grid(
                row=0, column=i)
            tk.Label(frame, text=str(i), font=("Consolas", 7), bg=bg, fg="#777777",
                     width=2).grid(row=1, column=i)
        return frame

    def _show_permuted(self, permuted, keyword_letters=0):
        for child in self.permuted_frame.winfo_children():
            child.destroy()
        self._alphabet_table(permuted, self.permuted_frame, keyword_letters).pack()
        if permuted:
            self.permuted_string.set(permuted)
        else:
            self.permuted_string.set("(enter a valid keyword to build it)")

    def _preview_alphabet(self):
        """Update the permuted alphabet live while the keyword is typed."""
        try:
            keyword = validate_keyword(self.keyword_entry.get())
        except ValueError:
            self._show_permuted(None)
            return
        permuted = build_permuted_alphabet(keyword)
        self._show_permuted(permuted, len(set(keyword)))

    def _update_button(self):
        is_encrypt = self.operation.get() == "encrypt"
        self.run_button.config(text="Encrypt" if is_encrypt else "Decrypt")
        self.input_label.config(text="Message:" if is_encrypt else "Ciphertext:")

    def _set_output(self, text):
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", text)
        self.output_text.config(state="disabled")

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
        try:
            k1 = validate_key(self.key_entry.get())
        except ValueError as e:
            self._error("Invalid key 1", str(e), self.key_entry)
            return
        try:
            keyword = validate_keyword(self.keyword_entry.get())
        except ValueError as e:
            self._show_permuted(None)
            self._error("Invalid key 2 (keyword)", str(e), self.keyword_entry)
            return
        try:
            text = prepare_text(self.input_text.get("1.0", "end-1c"))
        except ValueError as e:
            self._error("Invalid text", str(e), self.input_text)
            return

        permuted = build_permuted_alphabet(keyword)
        self._show_permuted(permuted, len(set(keyword)))

        if self.operation.get() == "encrypt":
            result = encrypt(text, k1, permuted)
            self.status.set(f"Encrypted with k1 = {k1}, k2 = {keyword}. Prepared plaintext: {text}")
        else:
            result = decrypt(text, k1, permuted)
            self.status.set(f"Decrypted with k1 = {k1}, k2 = {keyword}. Prepared ciphertext: {text}")
        self.status_label.config(fg="#2e7d32")
        self._set_output(result)

    def result_to_input(self):
        result = self.output_text.get("1.0", "end-1c")
        if not result:
            return
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", result)
        self.operation.set("decrypt" if self.operation.get() == "encrypt" else "encrypt")
        self._update_button()
        self._set_output("")

    def clear(self):
        self.key_entry.delete(0, "end")
        self.keyword_entry.delete(0, "end")
        self.input_text.delete("1.0", "end")
        self._set_output("")
        self._show_permuted(None)
        self.status.set("Choose an operation, enter key 1, key 2 (keyword) and the text.")
        self.status_label.config(fg="#555555")
        self.key_entry.focus_set()


if __name__ == "__main__":
    CaesarPermutationApp().mainloop()
