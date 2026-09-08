# ✂️ Diviser un tableau par colonne

**Divisez un fichier Excel, CSV ou JSON en plusieurs — un par valeur d'une colonne — directement dans votre navigateur. Sans installation, sans macro, sans VBA.**

[![Streamlit](https://img.shields.io/badge/Streamlit-application%20en%20ligne-FF4B4B?logo=streamlit&logoColor=white)](https://hakyemezi-filterandsave.streamlit.app)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![Licence : MIT](https://img.shields.io/badge/licence-MIT-green)](LICENSE)
[![Langues](https://img.shields.io/badge/interface-6%20langues-blueviolet)](#langues)

[🇬🇧 English](README.md) · [🇹🇷 Türkçe](README.tr.md) · **🇫🇷 Français** · [🇩🇪 Deutsch](README.de.md) · [🇪🇸 Español](README.es.md) · [🇮🇹 Italiano](README.it.md)

Vous avez un tableau de ventes de 40 000 lignes avec une colonne `région`, et il vous faut un fichier par région à envoyer à chaque agence. Dans Excel, cela fait un tableau croisé, un filtre, un copier, un coller et un enregistrement — quarante fois. Ici, c'est un glisser, un clic et un téléchargement.

**▶️ [Ouvrir l'application](https://hakyemezi-filterandsave.streamlit.app)** — déposez un fichier, sans inscription.

---

## Pourquoi cela vaut le détour

**Un seul classeur, une feuille par valeur.** C'est ce qu'un tableur ne peut pas faire sans écrire une macro. Au lieu de quarante fichiers, vous obtenez un `.xlsx` avec quarante onglets, chacun nommé d'après sa valeur et prêt à être transmis. Les noms de feuilles sont tronqués à la limite de 31 caractères d'Excel et dédoublonnés automatiquement.

**Diviser sur plusieurs colonnes à la fois.** Choisissez `région` *et* `année` et vous obtenez un groupe par combinaison — `Marmara - 2024`, `Marmara - 2025`, et ainsi de suite. C'est en le faisant à la main qu'on y passe l'après-midi.

**Voir le résultat avant que quoi que ce soit ne soit généré.** Un tableau de chaque groupe avec son nombre de lignes, ainsi que le nombre de groupes, les lignes couvertes, le plus grand groupe et le nombre de lignes ignorées. Si la division est mauvaise, vous le découvrez avant de télécharger, pas après avoir ouvert quarante fichiers.

**Retirer les colonnes qui ne doivent pas sortir.** Choisissez les colonnes qui figureront dans le résultat. Utile lorsque le tableau source contient des colonnes de coût ou de marge qui ne doivent pas quitter l'entreprise.

**L'application parle votre langue.** Toute l'interface est disponible en anglais, turc, français, allemand, espagnol et italien, listée avec les drapeaux dans la barre latérale. Les nombres suivent la convention de la langue choisie : 1 500 lignes s'écrit 1,500 en anglais et 1.500 en allemand.

**Elle gère ce qui casse les scripts naïfs.** Les valeurs contenant `/`, `\`, `:` ou `*` sont nettoyées avant de devenir des noms de fichier ou de feuille. Deux valeurs différentes qui aboutissent au même nom sont conservées séparément plutôt que de s'écraser silencieusement. Les valeurs vides peuvent être ignorées ou former leur propre groupe. Pour les classeurs à plusieurs feuilles, vous choisissez la feuille.

---

## Formats de sortie

| Option | Ce que vous obtenez | Quand l'utiliser |
|---|---|---|
| **Un seul classeur Excel, une feuille par groupe** | Un `.xlsx`, un onglet par valeur | Remettre un seul fichier à quelqu'un qui veut naviguer entre les groupes |
| **Fichiers Excel séparés dans un zip** | `Marmara.xlsx`, `Ege.xlsx`, … | Envoyer chaque groupe à une personne différente |
| **Fichiers CSV séparés dans un zip** | `Marmara.csv`, `Ege.csv`, … | Alimenter un autre système, ou traiter de très grands groupes |

La sortie CSV est écrite en UTF-8 avec BOM, afin que les caractères accentués s'ouvrent correctement dans Excel au lieu de se transformer en `Ã§`.

---

## L'exécuter chez vous

```bash
git clone https://github.com/hakyemezi/filterandsave.git
cd filterandsave
pip install -r requirements.txt
streamlit run filterandsave.py
```

Nécessite Python 3.9+. Les dépendances sont `streamlit`, `pandas` et `openpyxl` — rien d'autre.

Tout est construit en mémoire : rien n'est écrit sur le disque du serveur et les utilisateurs simultanés ne voient jamais les fichiers des autres.

---

## Comment l'utiliser

1. Déposez un fichier `.xlsx`, `.csv` ou `.json` (jusqu'à 200 Mo).
2. Si le classeur contient plusieurs feuilles, choisissez-en une.
3. Choisissez la colonne — ou les colonnes — sur laquelle diviser.
4. Choisissez éventuellement les colonnes à conserver dans le résultat.
5. Vérifiez le récapitulatif : combien de groupes, combien de lignes chacun.
6. Choisissez un classeur à plusieurs feuilles, ou un zip de fichiers séparés.
7. Téléchargez.

---

## Langues

L'interface est traduite en six langues. Toutes les six sont affichées avec leur drapeau dans la barre latérale, de sorte qu'un visiteur voit sa propre langue sans ouvrir de menu :

| Langue | Dans l'application | Cette page |
|---|---|---|
| 🇬🇧 **English** | Split a spreadsheet by column | [README.md](README.md) |
| 🇹🇷 **Türkçe** | Tabloyu sütuna göre böl | [README.tr.md](README.tr.md) |
| 🇫🇷 **Français** | Diviser un tableau par colonne | [README.fr.md](README.fr.md) |
| 🇩🇪 **Deutsch** | Tabelle nach Spalte aufteilen | [README.de.md](README.de.md) |
| 🇪🇸 **Español** | Dividir una hoja por columna | [README.es.md](README.es.md) |
| 🇮🇹 **Italiano** | Dividere un foglio per colonna | [README.it.md](README.it.md) |

Les traductions se trouvent dans [`translations.py`](translations.py), un dictionnaire par langue. Pour en ajouter une, copiez le bloc anglais, traduisez les valeurs et ajoutez une entrée à `LANGUAGES` avec le drapeau et le nom que la langue se donne à elle-même. Toute clé omise revient à l'anglais, si bien qu'une traduction partielle reste utilisable.

Les libellés du champ d'import proviennent de Streamlit lui-même et restent en anglais.

---

## Licence

[MIT](LICENSE)
