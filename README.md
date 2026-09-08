# ✂️ Split a spreadsheet by column

**Split one Excel, CSV or JSON file into many — one per value in a column — in your browser. No install, no macros, no VBA.**

[![Streamlit](https://img.shields.io/badge/Streamlit-live%20app-FF4B4B?logo=streamlit&logoColor=white)](https://hakyemezi-filterandsave.streamlit.app)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Languages](https://img.shields.io/badge/interface-6%20languages-blueviolet)](#languages)

You have a sales sheet with 40,000 rows and a `region` column, and you need one file per region to send to each office. In Excel that is a pivot, a filter, a copy, a paste and a save — forty times. Here it is a drag, a click and a download.

**▶️ [Open the app](https://hakyemezi-filterandsave.streamlit.app)** — drop a file in, no sign up.

---

## What makes it worth using

**One workbook, one sheet per value.** This is the part a spreadsheet cannot do for you without writing a macro. Instead of forty files, you get one `.xlsx` with forty tabs, named after each value and ready to hand over. Sheet names are truncated to Excel's 31-character limit and de-duplicated automatically.

**Split on more than one column at once.** Pick `region` *and* `year` and you get a group per combination — `Marmara - 2024`, `Marmara - 2025`, and so on. Doing that by hand is where the afternoon goes.

**See what you will get before it builds anything.** A table of every group and its row count, plus the number of groups, the rows covered, the largest group and how many rows were skipped. If the split is wrong you find out before you download, not after you open forty files.

**Drop columns you do not want to send out.** Choose which columns end up in the output. Useful when the source sheet has cost or margin columns that should not leave the building.

**It speaks your language.** The whole interface is available in English, Turkish, French, German, Spanish and Italian, listed with flags in the sidebar. Numbers follow the convention of the language you choose, so 1,500 rows becomes 1.500 in German and 1 500 in French.

**It handles the things that break naive scripts.** Values containing `/`, `\`, `:` or `*` are cleaned before they become file or sheet names. Two different values that clean up to the same name are kept apart rather than silently overwriting each other. Empty values can be skipped or kept as their own group. Multi-sheet workbooks let you pick the sheet.

---

## Output options

| Option | You get | Good for |
|---|---|---|
| **One Excel workbook, a sheet per group** | Single `.xlsx`, one tab per value | Handing one file to someone who wants to flip between groups |
| **Separate Excel files in a zip** | `Marmara.xlsx`, `Ege.xlsx`, … | Sending each group to a different person |
| **Separate CSV files in a zip** | `Marmara.csv`, `Ege.csv`, … | Feeding another system, or very large groups |

CSV output is written as UTF-8 with a BOM, so Turkish characters open correctly in Excel instead of turning into `Ã§`.

---

## Run it yourself

```bash
git clone https://github.com/hakyemezi/filterandsave.git
cd filterandsave
pip install -r requirements.txt
streamlit run filterandsave.py
```

Requires Python 3.9+. Dependencies are `streamlit`, `pandas` and `openpyxl` — nothing else.

Everything is built in memory, so nothing is written to disk on the server and concurrent users never see each other's files.

---

## How to use it

1. Drop in an `.xlsx`, `.csv` or `.json` file (up to 200 MB).
2. If the workbook has several sheets, pick one.
3. Choose the column — or columns — to split on.
4. Optionally choose which columns to keep in the output.
5. Check the summary: how many groups, how many rows each.
6. Choose one workbook with many sheets, or a zip of separate files.
7. Download.

---

## Languages

The interface is translated into six languages. All six are listed with their flags in the sidebar, so a visitor can see their own language without opening a menu:

| | |
|---|---|
| 🇬🇧 **English** | Split a spreadsheet by column |
| 🇹🇷 **Türkçe** | Tabloyu sütuna göre böl |
| 🇫🇷 **Français** | Diviser un tableau par colonne |
| 🇩🇪 **Deutsch** | Tabelle nach Spalte aufteilen |
| 🇪🇸 **Español** | Dividir una hoja por columna |
| 🇮🇹 **Italiano** | Dividere un foglio per colonna |

Translations live in [`translations.py`](translations.py) as one dictionary per language. To add another, copy the English block, translate the values, and add an entry to `LANGUAGES` with the flag and the language's own name for itself. Any key you leave out falls back to English, so a partial translation still works.

The file uploader's own labels come from Streamlit itself and stay in English.

---

## Türkçe

**Bir Excel, CSV veya JSON dosyasını bir sütundaki değerlere göre bölerek çok sayıda dosyaya ayırır.** Tarayıcıda çalışır, kurulum ve makro gerektirmez.

40.000 satırlık bir satış tablonuz ve bir `bölge` sütununuz var; her bölgeye ayrı dosya göndermeniz gerekiyor. Excel'de bu kırk kez filtrele-kopyala-yapıştır-kaydet demek. Burada sürükle, tıkla, indir.

- **Tek dosya, her grup için ayrı sekme** — Excel'in makro yazmadan yapamadığı şey. Kırk dosya yerine kırk sekmeli tek bir `.xlsx`. Sekme adları Excel'in 31 karakter sınırına göre kısaltılır ve çakışmalar otomatik çözülür.
- **Birden fazla sütuna göre bölme** — `bölge` ve `yıl` seçin, her kombinasyon için ayrı grup alın.
- **Üretmeden önce önizleme** — hangi grup kaç satır, kaç satır atlandı, hepsi indirmeden önce görünür.
- **İstemediğiniz sütunları çıkarın** — maliyet veya marj sütunları dışarı gitmesin.
- **Altı dil** — arayüz İngilizce, Türkçe, Fransızca, Almanca, İspanyolca ve İtalyanca. Kenar çubuğunda bayraklarıyla alt alta durur, sayılar da seçtiğiniz dilin biçimine uyar.
- **Türkçe karakterler** — CSV çıktısı UTF-8 BOM ile yazılır, Excel'de `Ã§` olmaz. Değerlerdeki `/` ve `:` gibi karakterler dosya adına dönüşmeden temizlenir.

---

## License

[MIT](LICENSE)
