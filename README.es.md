# ✂️ Dividir una hoja por columna

**Divide un archivo Excel, CSV o JSON en muchos — uno por cada valor de una columna — desde tu navegador. Sin instalar nada, sin macros, sin VBA.**

[![Streamlit](https://img.shields.io/badge/Streamlit-app%20en%20l%C3%ADnea-FF4B4B?logo=streamlit&logoColor=white)](https://hakyemezi-filterandsave.streamlit.app)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![Licencia: MIT](https://img.shields.io/badge/licencia-MIT-green)](LICENSE)
[![Idiomas](https://img.shields.io/badge/interfaz-6%20idiomas-blueviolet)](#idiomas)

[🇬🇧 English](README.md) · [🇹🇷 Türkçe](README.tr.md) · [🇫🇷 Français](README.fr.md) · [🇩🇪 Deutsch](README.de.md) · **🇪🇸 Español** · [🇮🇹 Italiano](README.it.md)

Tienes una hoja de ventas con 40.000 filas y una columna `región`, y necesitas un archivo por región para enviar a cada oficina. En Excel eso es una tabla dinámica, un filtro, un copiar, un pegar y un guardar — cuarenta veces. Aquí es arrastrar, hacer clic y descargar.

**▶️ [Abrir la aplicación](https://hakyemezi-filterandsave.streamlit.app)** — suelta un archivo, sin registro.

---

## Por qué merece la pena

**Un solo libro, una hoja por valor.** Esto es lo que una hoja de cálculo no puede hacer sin escribir una macro. En lugar de cuarenta archivos obtienes un `.xlsx` con cuarenta pestañas, cada una con el nombre de su valor y lista para entregar. Los nombres de hoja se recortan al límite de 31 caracteres de Excel y se hacen únicos automáticamente.

**Dividir por varias columnas a la vez.** Elige `región` *y* `año` y obtendrás un grupo por combinación — `Marmara - 2024`, `Marmara - 2025`, y así sucesivamente. Hacerlo a mano es lo que se lleva la tarde.

**Ver lo que vas a obtener antes de generar nada.** Una tabla con cada grupo y su número de filas, además del número de grupos, las filas incluidas, el grupo más grande y cuántas filas se omitieron. Si la división está mal, lo descubres antes de descargar y no después de abrir cuarenta archivos.

**Quitar las columnas que no deben salir.** Elige qué columnas acaban en el resultado. Útil cuando la hoja de origen tiene columnas de coste o margen que no deberían salir de la empresa.

**Habla tu idioma.** Toda la interfaz está disponible en inglés, turco, francés, alemán, español e italiano, listados con sus banderas en la barra lateral. Los números siguen la convención del idioma elegido: 1.500 filas se escribe 1,500 en inglés y 1 500 en francés.

**Resuelve lo que rompe a los scripts ingenuos.** Los valores que contienen `/`, `\`, `:` o `*` se limpian antes de convertirse en nombres de archivo o de hoja. Dos valores distintos que quedan con el mismo nombre se mantienen separados en lugar de sobrescribirse en silencio. Los valores vacíos se pueden omitir o conservar como su propio grupo. En libros con varias hojas, eliges la hoja.

---

## Formatos de salida

| Opción | Lo que obtienes | Cuándo usarlo |
|---|---|---|
| **Un solo libro de Excel, una hoja por grupo** | Un `.xlsx`, una pestaña por valor | Entregar un único archivo a alguien que quiere moverse entre grupos |
| **Archivos Excel separados en un zip** | `Marmara.xlsx`, `Ege.xlsx`, … | Enviar cada grupo a una persona distinta |
| **Archivos CSV separados en un zip** | `Marmara.csv`, `Ege.csv`, … | Alimentar otro sistema, o grupos muy grandes |

La salida CSV se escribe en UTF-8 con BOM, para que los acentos y la eñe se abran correctamente en Excel en lugar de convertirse en `Ã§`.

---

## Ejecutarlo tú mismo

```bash
git clone https://github.com/hakyemezi/filterandsave.git
cd filterandsave
pip install -r requirements.txt
streamlit run filterandsave.py
```

Requiere Python 3.9+. Las dependencias son `streamlit`, `pandas` y `openpyxl` — nada más.

Todo se construye en memoria, así que no se escribe nada en el disco del servidor y los usuarios simultáneos nunca ven los archivos de los demás.

---

## Cómo usarlo

1. Suelta un archivo `.xlsx`, `.csv` o `.json` (hasta 200 MB).
2. Si el libro tiene varias hojas, elige una.
3. Elige la columna — o las columnas — por las que dividir.
4. Si quieres, elige qué columnas se mantienen en el resultado.
5. Revisa el resumen: cuántos grupos y cuántas filas tiene cada uno.
6. Elige un libro con muchas hojas, o un zip con archivos separados.
7. Descarga.

---

## Idiomas

La interfaz está traducida a seis idiomas. Los seis aparecen con su bandera en la barra lateral, de modo que cada visitante ve su idioma sin abrir ningún menú:

| Idioma | En la aplicación | Esta página |
|---|---|---|
| 🇬🇧 **English** | Split a spreadsheet by column | [README.md](README.md) |
| 🇹🇷 **Türkçe** | Tabloyu sütuna göre böl | [README.tr.md](README.tr.md) |
| 🇫🇷 **Français** | Diviser un tableau par colonne | [README.fr.md](README.fr.md) |
| 🇩🇪 **Deutsch** | Tabelle nach Spalte aufteilen | [README.de.md](README.de.md) |
| 🇪🇸 **Español** | Dividir una hoja por columna | [README.es.md](README.es.md) |
| 🇮🇹 **Italiano** | Dividere un foglio per colonna | [README.it.md](README.it.md) |

Las traducciones están en [`translations.py`](translations.py), un diccionario por idioma. Para añadir otro, copia el bloque en inglés, traduce los valores y añade una entrada a `LANGUAGES` con la bandera y el nombre que el idioma se da a sí mismo. Cualquier clave que falte recurre al inglés, así que una traducción parcial sigue funcionando.

Las etiquetas del campo de carga vienen del propio Streamlit y permanecen en inglés.

---

## Licencia

[MIT](LICENSE)
