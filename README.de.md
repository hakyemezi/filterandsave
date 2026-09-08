# ✂️ Tabelle nach Spalte aufteilen

**Teilen Sie eine Excel-, CSV- oder JSON-Datei in viele auf — eine pro Wert einer Spalte — direkt im Browser. Ohne Installation, ohne Makros, ohne VBA.**

[![Streamlit](https://img.shields.io/badge/Streamlit-Live--App-FF4B4B?logo=streamlit&logoColor=white)](https://hakyemezi-filterandsave.streamlit.app)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![Lizenz: MIT](https://img.shields.io/badge/lizenz-MIT-green)](LICENSE)
[![Sprachen](https://img.shields.io/badge/oberfl%C3%A4che-6%20Sprachen-blueviolet)](#sprachen)

[🇬🇧 English](README.md) · [🇹🇷 Türkçe](README.tr.md) · [🇫🇷 Français](README.fr.md) · **🇩🇪 Deutsch** · [🇪🇸 Español](README.es.md) · [🇮🇹 Italiano](README.it.md)

Sie haben eine Umsatztabelle mit 40.000 Zeilen und einer Spalte `Region`, und Sie brauchen eine Datei pro Region für jede Niederlassung. In Excel sind das eine Pivot-Tabelle, ein Filter, ein Kopieren, ein Einfügen und ein Speichern — vierzig Mal. Hier sind es ein Ziehen, ein Klick und ein Download.

**▶️ [App öffnen](https://hakyemezi-filterandsave.streamlit.app)** — Datei hineinziehen, ohne Anmeldung.

---

## Warum sich das lohnt

**Eine Arbeitsmappe, ein Blatt pro Wert.** Das ist der Teil, den eine Tabellenkalkulation ohne Makro nicht leisten kann. Statt vierzig Dateien erhalten Sie eine `.xlsx` mit vierzig Registerkarten, jede nach ihrem Wert benannt und fertig zur Weitergabe. Blattnamen werden auf Excels Grenze von 31 Zeichen gekürzt und automatisch eindeutig gemacht.

**Nach mehreren Spalten gleichzeitig aufteilen.** Wählen Sie `Region` *und* `Jahr`, und Sie erhalten eine Gruppe je Kombination — `Marmara - 2024`, `Marmara - 2025` und so weiter. Von Hand geht dafür ein Nachmittag drauf.

**Sehen, was herauskommt, bevor etwas erzeugt wird.** Eine Tabelle mit jeder Gruppe und ihrer Zeilenzahl, dazu die Anzahl der Gruppen, die erfassten Zeilen, die größte Gruppe und wie viele Zeilen übersprungen wurden. Ist die Aufteilung falsch, merken Sie es vor dem Download und nicht erst, nachdem Sie vierzig Dateien geöffnet haben.

**Spalten entfernen, die das Haus nicht verlassen sollen.** Legen Sie fest, welche Spalten im Ergebnis landen. Nützlich, wenn die Quelltabelle Kosten- oder Margenspalten enthält.

**Sie spricht Ihre Sprache.** Die gesamte Oberfläche gibt es auf Englisch, Türkisch, Französisch, Deutsch, Spanisch und Italienisch, in der Seitenleiste mit Flaggen aufgelistet. Zahlen folgen der Konvention der gewählten Sprache: 1.500 Zeilen werden auf Englisch zu 1,500 und auf Französisch zu 1 500.

**Sie fängt ab, woran einfache Skripte scheitern.** Werte mit `/`, `\`, `:` oder `*` werden bereinigt, bevor sie zu Datei- oder Blattnamen werden. Zwei verschiedene Werte, die zum selben Namen führen, werden auseinandergehalten, statt sich still zu überschreiben. Leere Werte lassen sich überspringen oder als eigene Gruppe behalten. Bei Arbeitsmappen mit mehreren Blättern wählen Sie das Blatt aus.

---

## Ausgabeformate

| Option | Was Sie erhalten | Wofür |
|---|---|---|
| **Eine Excel-Arbeitsmappe, ein Blatt pro Gruppe** | Eine `.xlsx`, eine Registerkarte je Wert | Eine einzige Datei an jemanden geben, der zwischen den Gruppen wechseln möchte |
| **Einzelne Excel-Dateien in einem Zip** | `Marmara.xlsx`, `Ege.xlsx`, … | Jede Gruppe an eine andere Person schicken |
| **Einzelne CSV-Dateien in einem Zip** | `Marmara.csv`, `Ege.csv`, … | Ein anderes System beliefern oder sehr große Gruppen |

Die CSV-Ausgabe wird als UTF-8 mit BOM geschrieben, damit Umlaute und andere Sonderzeichen in Excel korrekt erscheinen statt als `Ã§`.

---

## Selbst ausführen

```bash
git clone https://github.com/hakyemezi/filterandsave.git
cd filterandsave
pip install -r requirements.txt
streamlit run filterandsave.py
```

Benötigt Python 3.9+. Abhängigkeiten sind `streamlit`, `pandas` und `openpyxl` — mehr nicht.

Alles wird im Arbeitsspeicher erzeugt. Auf dem Server wird nichts auf die Festplatte geschrieben, und gleichzeitige Nutzer sehen nie die Dateien der anderen.

---

## Bedienung

1. Ziehen Sie eine `.xlsx`-, `.csv`- oder `.json`-Datei hinein (bis 200 MB).
2. Hat die Arbeitsmappe mehrere Blätter, wählen Sie eines aus.
3. Wählen Sie die Spalte — oder die Spalten — zum Aufteilen.
4. Wählen Sie bei Bedarf, welche Spalten im Ergebnis bleiben.
5. Prüfen Sie die Übersicht: wie viele Gruppen, wie viele Zeilen je Gruppe.
6. Wählen Sie eine Arbeitsmappe mit vielen Blättern oder ein Zip mit einzelnen Dateien.
7. Herunterladen.

---

## Sprachen

Die Oberfläche ist in sechs Sprachen übersetzt. Alle sechs stehen mit ihrer Flagge in der Seitenleiste, sodass Besucher ihre Sprache sehen, ohne ein Menü zu öffnen:

| Sprache | In der App | Diese Seite |
|---|---|---|
| 🇬🇧 **English** | Split a spreadsheet by column | [README.md](README.md) |
| 🇹🇷 **Türkçe** | Tabloyu sütuna göre böl | [README.tr.md](README.tr.md) |
| 🇫🇷 **Français** | Diviser un tableau par colonne | [README.fr.md](README.fr.md) |
| 🇩🇪 **Deutsch** | Tabelle nach Spalte aufteilen | [README.de.md](README.de.md) |
| 🇪🇸 **Español** | Dividir una hoja por columna | [README.es.md](README.es.md) |
| 🇮🇹 **Italiano** | Dividere un foglio per colonna | [README.it.md](README.it.md) |

Die Übersetzungen liegen in [`translations.py`](translations.py), ein Wörterbuch je Sprache. Für eine weitere Sprache kopieren Sie den englischen Block, übersetzen die Werte und ergänzen `LANGUAGES` um einen Eintrag mit Flagge und der Eigenbezeichnung der Sprache. Fehlende Schlüssel fallen auf Englisch zurück, eine unvollständige Übersetzung bleibt also benutzbar.

Die Beschriftungen des Upload-Feldes stammen von Streamlit selbst und bleiben englisch.

---

## Lizenz

[MIT](LICENSE)
