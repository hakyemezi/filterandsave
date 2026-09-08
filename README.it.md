# ✂️ Dividere un foglio per colonna

**Dividi un file Excel, CSV o JSON in tanti file — uno per ogni valore di una colonna — direttamente nel browser. Senza installare nulla, senza macro, senza VBA.**

[![Streamlit](https://img.shields.io/badge/Streamlit-app%20online-FF4B4B?logo=streamlit&logoColor=white)](https://hakyemezi-filterandsave.streamlit.app)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![Licenza: MIT](https://img.shields.io/badge/licenza-MIT-green)](LICENSE)
[![Lingue](https://img.shields.io/badge/interfaccia-6%20lingue-blueviolet)](#lingue)

[🇬🇧 English](README.md) · [🇹🇷 Türkçe](README.tr.md) · [🇫🇷 Français](README.fr.md) · [🇩🇪 Deutsch](README.de.md) · [🇪🇸 Español](README.es.md) · **🇮🇹 Italiano**

Hai un foglio vendite con 40.000 righe e una colonna `regione`, e ti serve un file per ogni regione da mandare a ciascuna sede. In Excel significa una tabella pivot, un filtro, un copia, un incolla e un salvataggio — quaranta volte. Qui è un trascinamento, un clic e un download.

**▶️ [Apri l'applicazione](https://hakyemezi-filterandsave.streamlit.app)** — trascina un file, senza registrarti.

---

## Perché vale la pena

**Un'unica cartella di lavoro, un foglio per valore.** È la parte che un foglio di calcolo non può fare senza scrivere una macro. Invece di quaranta file ottieni un `.xlsx` con quaranta schede, ciascuna con il nome del proprio valore e pronta da consegnare. I nomi dei fogli vengono troncati al limite di 31 caratteri di Excel e resi univoci automaticamente.

**Dividere su più colonne insieme.** Scegli `regione` *e* `anno` e ottieni un gruppo per ogni combinazione — `Marmara - 2024`, `Marmara - 2025`, e così via. È farlo a mano che porta via il pomeriggio.

**Vedere cosa otterrai prima che venga generato qualcosa.** Una tabella con ogni gruppo e il suo numero di righe, più il numero di gruppi, le righe incluse, il gruppo più grande e quante righe sono state saltate. Se la divisione è sbagliata te ne accorgi prima di scaricare, non dopo aver aperto quaranta file.

**Togliere le colonne che non devono uscire.** Scegli quali colonne finiscono nel risultato. Utile quando il foglio di partenza contiene colonne di costo o di margine che non devono lasciare l'azienda.

**Parla la tua lingua.** L'intera interfaccia è disponibile in inglese, turco, francese, tedesco, spagnolo e italiano, elencate con le bandiere nella barra laterale. I numeri seguono la convenzione della lingua scelta: 1.500 righe diventa 1,500 in inglese e 1 500 in francese.

**Gestisce ciò su cui si rompono gli script ingenui.** I valori che contengono `/`, `\`, `:` o `*` vengono ripuliti prima di diventare nomi di file o di foglio. Due valori diversi che si riducono allo stesso nome restano separati invece di sovrascriversi in silenzio. I valori vuoti possono essere saltati o tenuti come gruppo a sé. Nelle cartelle con più fogli scegli tu il foglio.

---

## Formati di output

| Opzione | Cosa ottieni | Quando usarla |
|---|---|---|
| **Un'unica cartella di lavoro Excel, un foglio per gruppo** | Un `.xlsx`, una scheda per valore | Consegnare un solo file a chi vuole spostarsi tra i gruppi |
| **File Excel separati in uno zip** | `Marmara.xlsx`, `Ege.xlsx`, … | Mandare ogni gruppo a una persona diversa |
| **File CSV separati in uno zip** | `Marmara.csv`, `Ege.csv`, … | Alimentare un altro sistema, o gruppi molto grandi |

L'output CSV è scritto in UTF-8 con BOM, così le lettere accentate si aprono correttamente in Excel invece di diventare `Ã§`.

---

## Eseguirlo in locale

```bash
git clone https://github.com/hakyemezi/filterandsave.git
cd filterandsave
pip install -r requirements.txt
streamlit run filterandsave.py
```

Richiede Python 3.9+. Le dipendenze sono `streamlit`, `pandas` e `openpyxl` — nient'altro.

Tutto viene costruito in memoria: sul server non viene scritto nulla su disco e gli utenti collegati insieme non vedono mai i file degli altri.

---

## Come si usa

1. Trascina un file `.xlsx`, `.csv` o `.json` (fino a 200 MB).
2. Se la cartella di lavoro ha più fogli, scegline uno.
3. Scegli la colonna — o le colonne — su cui dividere.
4. Se vuoi, scegli quali colonne tenere nel risultato.
5. Controlla il riepilogo: quanti gruppi e quante righe ciascuno.
6. Scegli un'unica cartella con molti fogli, oppure uno zip di file separati.
7. Scarica.

---

## Lingue

L'interfaccia è tradotta in sei lingue. Tutte e sei compaiono con la loro bandiera nella barra laterale, così chi arriva vede la propria lingua senza aprire alcun menu:

| Lingua | Nell'applicazione | Questa pagina |
|---|---|---|
| 🇬🇧 **English** | Split a spreadsheet by column | [README.md](README.md) |
| 🇹🇷 **Türkçe** | Tabloyu sütuna göre böl | [README.tr.md](README.tr.md) |
| 🇫🇷 **Français** | Diviser un tableau par colonne | [README.fr.md](README.fr.md) |
| 🇩🇪 **Deutsch** | Tabelle nach Spalte aufteilen | [README.de.md](README.de.md) |
| 🇪🇸 **Español** | Dividir una hoja por columna | [README.es.md](README.es.md) |
| 🇮🇹 **Italiano** | Dividere un foglio per colonna | [README.it.md](README.it.md) |

Le traduzioni si trovano in [`translations.py`](translations.py), un dizionario per lingua. Per aggiungerne un'altra, copia il blocco inglese, traduci i valori e aggiungi una voce a `LANGUAGES` con la bandiera e il nome che la lingua dà a sé stessa. Ogni chiave mancante ricade sull'inglese, quindi una traduzione parziale resta utilizzabile.

Le etichette del campo di caricamento provengono da Streamlit stesso e restano in inglese.

---

## Licenza

[MIT](LICENSE)
