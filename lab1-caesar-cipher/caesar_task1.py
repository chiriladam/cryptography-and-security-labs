"""
Laboratory Work No. 1 - Task 1.1
Caesar cipher over the Romanian alphabet (n = 31), with a simple Tkinter GUI.

Author: Macari Chiril-Adam, FAF-243
"""

import re
import tkinter as tk
import unicodedata
from tkinter import messagebox

# ---------------------------------------------------------------------------
# 1. Letter encoding (Table 2): A = 0, Ă = 1, Â = 2, ..., Z = 30
#    The shift is computed ONLY with these codes, never with ord()/chr().
# ---------------------------------------------------------------------------
ALPHABET = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"
N = len(ALPHABET)  # 31

LETTER_TO_CODE = {letter: code for code, letter in enumerate(ALPHABET)}
CODE_TO_LETTER = {code: letter for code, letter in enumerate(ALPHABET)}

# Ş/Ţ typed with a cedilla are treated as Ș/Ț (comma below).
CEDILLA_FIX = {"Ş": "Ș", "ş": "ș", "Ţ": "Ț", "ţ": "ț"}

# Every character the user is allowed to type: the 31 letters in both cases.
ALLOWED_LETTERS = set(ALPHABET) | set(ALPHABET.lower())
WHITESPACE = {" ", "\n", "\t", "\r"}

KEY_MIN, KEY_MAX = 1, N - 1  # 1 .. 30


def mod(a, n):
    """Modulo that always returns a value in 0..n-1, even when a is negative."""
    r = a % n
    if r < 0:  # some languages return negative remainders; guard it explicitly
        r += n
    return r


# ---------------------------------------------------------------------------
# 2. Input validation
# ---------------------------------------------------------------------------
def validate_key(raw):
    """Return the key as int, or raise ValueError with a clear message."""
    value = raw.strip()
    if not re.fullmatch(r"[0-9]+", value):
        raise ValueError(
            f"Invalid key: '{raw}'.\n\n"
            f"The key must be an integer between {KEY_MIN} and {KEY_MAX} (inclusive)."
        )
    key = int(value)
    if not KEY_MIN <= key <= KEY_MAX:
        raise ValueError(
            f"Invalid key: {key} is out of range.\n\n"
            f"The key must be an integer between {KEY_MIN} and {KEY_MAX} (inclusive)."
        )
    return key


def prepare_text(raw):
    """Validate the text, then convert it to uppercase and remove the spaces.

    Raises ValueError naming the first rejected character.
    """
    text = unicodedata.normalize("NFC", raw)
    text = "".join(CEDILLA_FIX.get(ch, ch) for ch in text)

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
# 3. Encryption / decryption
#    c = (x + k) mod n        m = (y - k) mod n
# ---------------------------------------------------------------------------
def encrypt(plaintext, k):
    result = []
    for letter in plaintext:
        x = LETTER_TO_CODE[letter]
        c = mod(x + k, N)
        result.append(CODE_TO_LETTER[c])
    return "".join(result)


def decrypt(ciphertext, k):
    result = []
    for letter in ciphertext:
        y = LETTER_TO_CODE[letter]
        m = mod(y - k, N)
        result.append(CODE_TO_LETTER[m])
    return "".join(result)


# ---------------------------------------------------------------------------
# 4. GUI
# ---------------------------------------------------------------------------
BG = "#f4f5f7"
CARD = "#ffffff"
ACCENT = "#1f5fa8"
ERROR = "#c62828"
FONT = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
MONO = ("Consolas", 11)


class CaesarApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lab 1 - Task 1.1 - Caesar Cipher (Romanian alphabet)")
        self.configure(bg=BG, padx=16, pady=14)
        self.resizable(False, False)

        self.operation = tk.StringVar(value="encrypt")
        self.status = tk.StringVar(value="Choose an operation, enter the key and the text.")

        tk.Label(self, text="Caesar Cipher - Romanian alphabet (n = 31)",
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

        # Key
        tk.Label(self, text="Key k (1-30):", font=FONT_BOLD, bg=BG).grid(
            row=2, column=0, sticky="w", pady=6, padx=(0, 10))
        self.key_entry = tk.Entry(self, width=8, font=MONO, relief="solid", bd=1)
        self.key_entry.grid(row=2, column=1, sticky="w", pady=6)

        # Input text
        self.input_label = tk.Label(self, text="Message:", font=FONT_BOLD, bg=BG)
        self.input_label.grid(row=3, column=0, sticky="nw", pady=(4, 0))
        self.input_text = tk.Text(self, width=58, height=4, font=MONO, wrap="word",
                                  relief="solid", bd=1)
        self.input_text.grid(row=3, column=1, sticky="w", pady=(4, 0))

        # Buttons
        buttons = tk.Frame(self, bg=BG)
        buttons.grid(row=4, column=1, sticky="w", pady=10)
        self.run_button = tk.Button(buttons, text="Encrypt", width=12, font=FONT_BOLD,
                                    bg=ACCENT, fg="white", activebackground="#174a85",
                                    activeforeground="white", relief="flat",
                                    command=self.run)
        self.run_button.pack(side="left")
        tk.Button(buttons, text="Use result as input", font=FONT, relief="groove",
                  command=self.result_to_input).pack(side="left", padx=8)
        tk.Button(buttons, text="Clear", font=FONT, relief="groove",
                  command=self.clear).pack(side="left")

        # Result
        tk.Label(self, text="Result:", font=FONT_BOLD, bg=BG).grid(row=5, column=0, sticky="nw")
        self.output_text = tk.Text(self, width=58, height=4, font=MONO, wrap="char",
                                   relief="solid", bd=1, bg="#eef3fa", state="disabled")
        self.output_text.grid(row=5, column=1, sticky="w")

        # Alphabet table (Table 2) for checking by hand
        tk.Label(self, text="Alphabet:", font=FONT_BOLD, bg=BG).grid(
            row=6, column=0, sticky="nw", pady=(12, 0))
        self._alphabet_table(ALPHABET).grid(row=6, column=1, sticky="w", pady=(12, 0))

        # Status line
        self.status_label = tk.Label(self, textvariable=self.status, font=FONT, bg=BG,
                                     fg="#555555", anchor="w", justify="left")
        self.status_label.grid(row=7, column=0, columnspan=2, sticky="we", pady=(10, 0))

        self.bind("<Return>", lambda _e: self.run())
        self.key_entry.focus_set()

    def _alphabet_table(self, letters):
        frame = tk.Frame(self, bg=CARD, highlightbackground="#c9ced6", highlightthickness=1)
        for i, letter in enumerate(letters):
            tk.Label(frame, text=letter, font=("Consolas", 9, "bold"), bg=CARD, width=2).grid(
                row=0, column=i)
            tk.Label(frame, text=str(i), font=("Consolas", 7), bg=CARD, fg="#777777",
                     width=2).grid(row=1, column=i)
        return frame

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
        # ask for the value again: focus and select the wrong field
        widget.focus_set()
        if isinstance(widget, tk.Entry):
            widget.select_range(0, "end")
        else:
            widget.tag_add("sel", "1.0", "end-1c")

    def run(self):
        try:
            k = validate_key(self.key_entry.get())
        except ValueError as e:
            self._error("Invalid key", str(e), self.key_entry)
            return
        try:
            text = prepare_text(self.input_text.get("1.0", "end-1c"))
        except ValueError as e:
            self._error("Invalid text", str(e), self.input_text)
            return

        if self.operation.get() == "encrypt":
            result = encrypt(text, k)
            self.status.set(f"Encrypted with k = {k}. Prepared plaintext: {text}")
        else:
            result = decrypt(text, k)
            self.status.set(f"Decrypted with k = {k}. Prepared ciphertext: {text}")
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
        self.input_text.delete("1.0", "end")
        self._set_output("")
        self.status.set("Choose an operation, enter the key and the text.")
        self.status_label.config(fg="#555555")
        self.key_entry.focus_set()


if __name__ == "__main__":
    CaesarApp().mainloop()
