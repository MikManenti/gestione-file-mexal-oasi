import csv
import os
import tkinter as tk
from tkinter import filedialog, messagebox

import pandas as pd


class ConverterApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Convertitore funzioni TXT/XLS in CSV")
        self.root.geometry("540x260")
        self.root.resizable(False, False)

        self.mexal_mode_var = tk.BooleanVar(value=False)
        self.copreweb_mode_var = tk.BooleanVar(value=False)
        self.selected_file_var = tk.StringVar(value="Nessun file selezionato")

        self._build_ui()

    def _build_ui(self) -> None:
        title = tk.Label(
            self.root,
            text="Converti file standard in .csv",
            font=("Segoe UI", 13, "bold"),
        )
        title.pack(pady=(14, 10))

        mode_check = tk.Checkbutton(
            self.root,
            text="Scenario 1 - Bolla Mexal (TXT a lunghezza fissa)",
            variable=self.mexal_mode_var,
            font=("Segoe UI", 10, "bold"),
        )
        mode_check.pack(pady=(0, 8))

        copreweb_check = tk.Checkbutton(
            self.root,
            text="Scenario 2 - Volantino (Copreweb)",
            variable=self.copreweb_mode_var,
            font=("Segoe UI", 10, "bold"),
        )
        copreweb_check.pack(pady=(0, 8))

        choose_btn = tk.Button(
            self.root,
            text="1) Scegli file di input",
            command=self.choose_file,
            width=28,
            font=("Segoe UI", 10),
        )
        choose_btn.pack(pady=(12, 6))

        selected_label = tk.Label(
            self.root,
            textvariable=self.selected_file_var,
            wraplength=500,
            justify=tk.CENTER,
            font=("Segoe UI", 9),
        )
        selected_label.pack(pady=(4, 10))

        convert_btn = tk.Button(
            self.root,
            text="2) Converti in CSV",
            command=self.convert_file,
            width=28,
            bg="#1f6feb",
            fg="white",
            activebackground="#1757b4",
            font=("Segoe UI", 10, "bold"),
        )
        convert_btn.pack(pady=6)

        hint = tk.Label(
            self.root,
            text="Bolla Mexal usa TXT. Volantino (Copreweb) usa Excel e produce CSV con colonne I e Y.",
            font=("Segoe UI", 9, "italic"),
            fg="#444",
        )
        hint.pack(pady=(10, 0))

    def _read_txt_to_dataframe(self, file_path: str) -> pd.DataFrame:
        # Prova automaticamente separatori comuni in ordine di probabilita.
        delimiters = [";", "\t", ",", "|"]

        for delimiter in delimiters:
            try:
                df = pd.read_csv(file_path, sep=delimiter, dtype=str, encoding="utf-8")
                if df.shape[1] > 1:
                    return df
            except Exception:
                continue

        # Fallback: una colonna unica, ogni riga del file.
        rows = []
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                rows.append([line.rstrip("\n")])

        return pd.DataFrame(rows, columns=["contenuto"])

    def _read_excel_to_dataframe(self, file_path: str) -> pd.DataFrame:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".xls":
            return pd.read_excel(file_path, dtype=str, engine="xlrd")
        return pd.read_excel(file_path, dtype=str)

    def _slice_1_based(self, text: str, start: int, end: int) -> str:
        if end < start:
            return ""
        return text[start - 1 : end]

    def _sanitize_filename_part(self, value: str) -> str:
        invalid = '<>:"/\\|?*'
        cleaned = "".join("_" if ch in invalid else ch for ch in value.strip())
        return cleaned if cleaned else "output"

    def _format_currency_value(self, value: str) -> str:
        digits_only = "".join(ch for ch in value if ch.isdigit())
        if not digits_only:
            return "0,00"

        amount = int(digits_only) / 100
        return f"{amount:.2f}".replace(".", ",")

    def _format_numeric_value(self, value: str) -> str:
        digits_only = "".join(ch for ch in value if ch.isdigit())
        if not digits_only:
            return "0"

        return str(int(digits_only))

    def _convert_mexal_bolla(self, input_file: str) -> str:
        with open(input_file, "r", encoding="utf-8", errors="replace") as f:
            lines = [line.rstrip("\n") for line in f if line.strip()]

        if not lines:
            raise ValueError("Il file TXT e' vuoto.")

        first_line = lines[0]
        suffix = self._sanitize_filename_part(self._slice_1_based(first_line, 114, 123))

        base_name = os.path.splitext(os.path.basename(input_file))[0]
        out_name = f"{base_name}_{suffix}.csv"
        out_file = os.path.join(os.path.dirname(input_file), out_name)

        rows = []
        for line in lines:
            # Mantiene solo i campi richiesti secondo posizioni 1-based inclusive.
            field_1 = self._slice_1_based(line, 31, 43).strip()
            raw_field_2 = self._slice_1_based(line, 94, 103).strip()
            field_2 = self._format_currency_value(raw_field_2)
            raw_field_3 = self._slice_1_based(line, 104, 113).strip()
            field_3 = self._format_numeric_value(raw_field_3)
            rows.append([field_1, field_2, field_3])

        with open(out_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter=";", quoting=csv.QUOTE_MINIMAL)
            writer.writerows(rows)

        return out_file

    def _convert_copreweb(self, input_file: str, out_file: str) -> None:
        df = pd.read_excel(input_file, header=None, dtype=str)

        if df.shape[1] <= 24:
            raise ValueError("Il file Excel non contiene le colonne I e Y richieste.")

        simplified = df.iloc[1:, [8, 24]].fillna("")
        simplified.to_csv(
            out_file,
            index=False,
            header=False,
            sep=";",
            encoding="utf-8",
            quoting=csv.QUOTE_MINIMAL,
        )

    def convert_file(self) -> None:
        input_file = self.selected_file_var.get()

        if input_file == "Nessun file selezionato" or not os.path.isfile(input_file):
            messagebox.showwarning("Attenzione", "Seleziona prima un file di input valido.")
            return

        if self.mexal_mode_var.get() and self.copreweb_mode_var.get():
            messagebox.showwarning(
                "Attenzione",
                "Seleziona un solo scenario speciale alla volta.",
            )
            return

        if not self.mexal_mode_var.get() and not self.copreweb_mode_var.get():
            messagebox.showwarning(
                "Attenzione",
                "Seleziona una funzione: Bolla Mexal o Volantino (Copreweb).",
            )
            return

        try:
            if self.mexal_mode_var.get():
                out_file = self._convert_mexal_bolla(input_file)
            else:
                out_file = filedialog.asksaveasfilename(
                    title="Salva CSV come",
                    defaultextension=".csv",
                    filetypes=[("CSV files", "*.csv")],
                )

                if not out_file:
                    return

                if self.copreweb_mode_var.get():
                    self._convert_copreweb(input_file, out_file)
                else:
                    raise ValueError("Funzione non supportata.")

            messagebox.showinfo("Completato", f"File CSV creato con successo:\n{out_file}")

        except Exception as exc:
            messagebox.showerror("Errore", f"Conversione non riuscita:\n{exc}")

    def choose_file(self) -> None:
        if self.mexal_mode_var.get():
            filetypes = [("Text files", "*.txt")]
        elif self.copreweb_mode_var.get():
            filetypes = [("Excel files", "*.xls *.xlsx")]
        else:
            messagebox.showwarning(
                "Attenzione",
                "Seleziona prima una funzione: Bolla Mexal o Volantino (Copreweb).",
            )
            return

        file_path = filedialog.askopenfilename(
            title="Seleziona il file di input",
            filetypes=filetypes,
        )

        if file_path:
            self.selected_file_var.set(file_path)


def main() -> None:
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
