# gestione-file-mexal-oasi

Programma con interfaccia grafica per convertire file standard in `.csv` in base alla funzione selezionata.

## Funzionalita

- Checkbox dedicata allo Scenario 1: Bolla Mexal
- Checkbox dedicata allo Scenario 2: Volantino (Copreweb)
- Apertura file guidata
- Conversione in CSV secondo la funzione selezionata
- Gestione base degli errori a schermo

## Requisiti

- Python 3.10+ (consigliato)
- Windows (se vuoi creare ed eseguire il `.exe`)

## Avvio rapido (sviluppo)

1. Crea e attiva un virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
```

Su Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Installa le dipendenze:

```bash
pip install -r requirements.txt
```

3. Avvia il programma:

```bash
python converter_gui.py
```

## Creazione dell'eseguibile `.exe` (Windows)

Hai due opzioni.

### Opzione A: script automatico

Nel prompt dei comandi di Windows:

```bat
build_exe.bat
```

Lo script ora si interrompe al primo errore e mostra un messaggio chiaro se una dipendenza non si installa.

Al termine troverai l'eseguibile in:

- `dist\ConvertitoreCSV.exe`

### Opzione B: comando manuale

```bat
py -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
python -m PyInstaller --noconfirm --onefile --windowed --name ConvertitoreCSV converter_gui.py
```

### Risoluzione problemi build su Windows

- Se vedi errori `meson`/`vswhere.exe` durante l'installazione di `pandas`, significa che `pip` sta tentando una compilazione da sorgente.
- Se il tuo Python non trova `pandas==2.2.x`, usa il vincolo presente in `requirements.txt` (`pandas>=2.3.3,<3.0`) e riprova.
- Lo script usa `python -m PyInstaller`, quindi non dipende da `pyinstaller` nel `PATH`.

## Note sulla conversione

- Per i `.txt`, il programma prova separatori comuni (`;`, tab, `,`, `|`).
- Se non riesce a identificare un separatore, salva ogni riga come singola colonna.
- Per i `.xls` usa il motore `xlrd`; per `.xlsx` usa `openpyxl`.

### Scenario 1 - Bolla Mexal

Se attivi la checkbox "Scenario 1 - Bolla Mexal (TXT a lunghezza fissa)", il programma:

- accetta solo input `.txt`
- per ogni riga mantiene i caratteri:
1. dal 31 al 43
2. dal 94 al 103
3. dal 104 al 113
- scrive questi 3 valori in CSV separati da `;`
- il secondo valore viene trattato come valuta: il numero viene diviso per 100 e scritto con la virgola decimale
- il terzo valore viene trattato come numerico e viene scritto senza zeri iniziali
- crea automaticamente il nome del file output come:
	- `nomeFileOriginale_XXXXXXXXXX.csv`
	- dove `XXXXXXXXXX` sono i caratteri dal 114 al 123 della prima riga

Il CSV viene salvato nella stessa cartella del file `.txt` di input.

### Scenario 2 - Volantino (Copreweb)

Se attivi la checkbox "Scenario 2 - Volantino (Copreweb)", il programma:

- accetta input `.xls` o `.xlsx`
- mantiene solo le colonne Excel `I` e `Y`
- le esporta in questo ordine: `I`, `Y`
- elimina la prima riga del file, considerata intestazione
- genera un CSV senza intestazione
- usa `;` come separatore nel file CSV

In questo scenario scegli manualmente il nome e il percorso del file CSV di output.