import tkinter as tk
from tkinter import ttk, messagebox
from zxcvbn import zxcvbn
import random
import string

MAX_PASS_LEN = 72
DEFAULT_PASS_LEN = 32
MIN_PASS_LEN = 8
MAX_GEN_PASS_LEN = 72
class PasswortCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Passwort-Sicherheitsprüfung")
        self.root.geometry("640x700")
        self.root.resizable(False, False)
        self.theme = "light"

        self.style = ttk.Style()
        self.set_theme(self.theme)

        self.build_gui()
        self.zentriere_fenster()
        self.text_eingabe.focus()

    def build_gui(self):
        self.rahmen = ttk.Frame(self.root, padding=15)
        self.rahmen.pack(expand=True, fill="both")

        # Passwortfeld
        ttk.Label(self.rahmen, text="🔑 Passwort eingeben:").pack(anchor="w")
        self.text_eingabe = tk.Text(self.rahmen, width=40, height=2, font=("Arial", 12))
        self.text_eingabe.pack(pady=5)
        self.text_eingabe.bind("<KeyRelease>", lambda e: self.bewerte_passwort())

        # Passwort anzeigen Checkbox
        self.show_var = tk.BooleanVar(value=False)
        self.check_show = ttk.Checkbutton(self.rahmen, text="Passwort anzeigen", variable=self.show_var, command=self.toggle_passwort)
        self.check_show.pack(anchor="w", pady=(0, 10))

        # Fortschrittsbalken
        self.staerke_bar = ttk.Progressbar(self.rahmen, length=400, maximum=4)
        self.staerke_bar.pack(pady=(10, 0))

        # Ergebnislabels
        self.ergebnis_var = tk.StringVar()
        self.zeit_var = tk.StringVar()
        self.details_var = tk.StringVar()
        self.empfehlung_var = tk.StringVar()

        self.label_ergebnis = ttk.Label(self.rahmen, textvariable=self.ergebnis_var, font=("Arial", 14, "bold"))
        self.label_ergebnis.pack(pady=(10, 0))

        ttk.Label(self.rahmen, textvariable=self.zeit_var).pack()
        ttk.Label(self.rahmen, textvariable=self.details_var, font=("Arial", 10)).pack(pady=(5, 0))
        ttk.Label(self.rahmen, textvariable=self.empfehlung_var, font=("Arial", 10), foreground="purple").pack(pady=(5, 0))

        # Buttonzeile
        button_frame = ttk.Frame(self.rahmen)
        button_frame.pack(pady=10, fill="x")
        ttk.Button(button_frame, text="Prüfen", command=self.bewerte_passwort).pack(side="left", expand=True, fill="x", padx=5)
        ttk.Button(button_frame, text="Zurücksetzen", command=self.clear_passwort).pack(side="left", expand=True, fill="x", padx=5)
        ttk.Button(button_frame, text="Passwort kopieren", command=self.copy_passwort).pack(side="left", expand=True, fill="x", padx=5)
        ttk.Button(button_frame, text="Ergebnis kopieren", command=self.copy_ergebnis).pack(side="left", expand=True, fill="x", padx=5)

        # Passwortgenerator Optionen
        ttk.Label(self.rahmen, text="🔧 Passwort-Generator Optionen:").pack(anchor="w", pady=(10, 0))

        self.include_upper = tk.BooleanVar(value=True)
        self.include_lower = tk.BooleanVar(value=True)
        self.include_digits = tk.BooleanVar(value=True)
        self.include_symbols = tk.BooleanVar(value=True)

        option_frame = ttk.Frame(self.rahmen)
        option_frame.pack(anchor="w", padx=5)

        ttk.Checkbutton(option_frame, text="Großbuchstaben", variable=self.include_upper).grid(row=0, column=0, sticky="w", padx=5)
        ttk.Checkbutton(option_frame, text="Kleinbuchstaben", variable=self.include_lower).grid(row=0, column=1, sticky="w", padx=5)
        ttk.Checkbutton(option_frame, text="Zahlen", variable=self.include_digits).grid(row=1, column=0, sticky="w", padx=5)
        ttk.Checkbutton(option_frame, text="Sonderzeichen", variable=self.include_symbols).grid(row=1, column=1, sticky="w", padx=5)

        # Spinbox für Passwortlänge
        spinbox_frame = ttk.Frame(self.rahmen)
        spinbox_frame.pack(anchor="w", pady=(10, 0), padx=5)
        ttk.Label(spinbox_frame, text="Länge des generierten Passworts:").pack(side="left")
        self.pass_len_var = tk.IntVar(value=DEFAULT_PASS_LEN)
        self.spin_pass_len = ttk.Spinbox(
            spinbox_frame, from_=MIN_PASS_LEN, to=MAX_GEN_PASS_LEN,
            textvariable=self.pass_len_var, width=5
        )
        self.spin_pass_len.pack(side="left", padx=5)

        # Generator Button
        ttk.Button(self.rahmen, text="🔁 Generiere sicheres Passwort", command=self.generiere_passwort).pack(pady=10)

        # Theme Umschalter
        self.theme_var = tk.StringVar(value="light")
        theme_frame = ttk.Frame(self.rahmen)
        theme_frame.pack(anchor="e", pady=(5, 0))
        ttk.Label(theme_frame, text="Theme:").pack(side="left")
        ttk.Radiobutton(theme_frame, text="Hell", variable=self.theme_var, value="light", command=self.change_theme).pack(side="left")
        ttk.Radiobutton(theme_frame, text="Dunkel", variable=self.theme_var, value="dark", command=self.change_theme).pack(side="left")

    def set_theme(self, theme):
        if theme == "dark":
            self.style.theme_use('clam')
            self.style.configure('.', background='#2e2e2e', foreground='white')
            self.style.configure('TLabel', background='#2e2e2e', foreground='white')
            self.style.configure('TButton', background='#454545', foreground='white')
            self.style.configure('TCheckbutton', background='#2e2e2e', foreground='white')
            self.root.configure(bg='#2e2e2e')
        else:
            self.style.theme_use('default')
            self.style.configure('.', background='SystemButtonFace', foreground='black')
            self.root.configure(bg='SystemButtonFace')

    def change_theme(self):
        self.set_theme(self.theme_var.get())

    def toggle_passwort(self):
        if self.show_var.get():
            messagebox.showinfo("Hinweis", "Mehrzeilige Passworteingabe kann nicht maskiert werden.")

    def bewerte_passwort(self, event=None):
        pw = self.text_eingabe.get("1.0", "end-1c").strip()
        if not pw:
            self.set_ergebnis("⚠️ Bitte ein Passwort eingeben", "orange")
            self.staerke_bar['value'] = 0
            self.set_zeit("")
            self.set_details("")
            self.set_empfehlung("")
            return

        if len(pw) > MAX_PASS_LEN:
            pw = pw[:MAX_PASS_LEN]
            self.set_ergebnis(f"⚠️ Passwortanalyse auf {MAX_PASS_LEN} Zeichen begrenzt", "orange")
        else:
            self.set_ergebnis("")

        result = zxcvbn(pw)
        score = result['score']
        crack_time = result['crack_times_display']['offline_slow_hashing_1e4_per_second']
        bewertung = ["🔴 Sehr schwach", "🟠 Schwach", "🟡 Mittel", "🟢 Stark", "🔵 Sehr stark"]
        farben = ["red", "orange", "gold", "green", "blue"]

        self.set_ergebnis(f"Sicherheit: {bewertung[score]}", farben[score])
        self.set_zeit(f"Geschätzte Knackzeit: {crack_time}")
        self.staerke_bar['value'] = score + 1

        details = f"Länge: {len(pw)} | "
        details += " ".join([
            "Großbuchstaben" if any(c.isupper() for c in pw) else "",
            "Kleinbuchstaben" if any(c.islower() for c in pw) else "",
            "Zahlen" if any(c.isdigit() for c in pw) else "",
            "Sonderzeichen" if any(not c.isalnum() for c in pw) else ""
        ]).strip()
        self.set_details(details)

        # Empfehlungen
        empfehlungen = []
        if len(pw) < 12: empfehlungen.append("🔸 Länger als 12 Zeichen verwenden")
        if not any(c.isupper() for c in pw): empfehlungen.append("🔸 Großbuchstaben hinzufügen")
        if not any(c.islower() for c in pw): empfehlungen.append("🔸 Kleinbuchstaben hinzufügen")
        if not any(c.isdigit() for c in pw): empfehlungen.append("🔸 Zahlen hinzufügen")
        if not any(not c.isalnum() for c in pw): empfehlungen.append("🔸 Sonderzeichen verwenden")
        if not empfehlungen: empfehlungen.append("✅ Sehr gutes Passwort!")
        self.set_empfehlung("\n".join(empfehlungen))

    def set_ergebnis(self, text, farbe="black"):
        self.ergebnis_var.set(text)
        self.label_ergebnis.config(foreground=farbe)

    def set_zeit(self, text): self.zeit_var.set(text)
    def set_details(self, text): self.details_var.set(text)
    def set_empfehlung(self, text): self.empfehlung_var.set(text)

    def clear_passwort(self):
        self.text_eingabe.delete("1.0", "end")
        self.set_ergebnis("")
        self.set_zeit("")
        self.set_details("")
        self.set_empfehlung("")
        self.staerke_bar['value'] = 0

    def copy_passwort(self):
        pw = self.text_eingabe.get("1.0", "end-1c")
        if pw:
            self.root.clipboard_clear()
            self.root.clipboard_append(pw)
            messagebox.showinfo("Kopiert", "Passwort wurde kopiert.")

    def copy_ergebnis(self):
        text = "\n".join([
            self.ergebnis_var.get(),
            self.zeit_var.get(),
            self.details_var.get(),
            self.empfehlung_var.get()
        ])
        if text.strip():
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            messagebox.showinfo("Kopiert", "Ergebnis wurde kopiert.")

    def generiere_passwort(self):
        zeichen = ""
        if self.include_upper.get(): zeichen += string.ascii_uppercase
        if self.include_lower.get(): zeichen += string.ascii_lowercase
        if self.include_digits.get(): zeichen += string.digits
        if self.include_symbols.get(): zeichen += "!@#$%^&*()-_=+[]{};:,.<>?/|"

        if not zeichen:
            messagebox.showwarning("Fehler", "Bitte mindestens eine Option auswählen.")
            return

        # Länge aus Spinbox auslesen
        länge = self.pass_len_var.get()
        if länge < MIN_PASS_LEN or länge > MAX_GEN_PASS_LEN:
            messagebox.showwarning("Fehler", f"Bitte Länge zwischen {MIN_PASS_LEN} und {MAX_GEN_PASS_LEN} wählen.")
            return

        pw = ''.join(random.choice(zeichen) for _ in range(länge))
        self.text_eingabe.delete("1.0", "end")
        self.text_eingabe.insert("1.0", pw)
        self.bewerte_passwort()

    def zentriere_fenster(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswortCheckerApp(root)
    root.mainloop()
