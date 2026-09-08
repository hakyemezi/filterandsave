# ✂️ Tabloyu sütuna göre böl

**Bir Excel, CSV veya JSON dosyasını, bir sütundaki her değer için ayrı dosyaya bölün — tarayıcınızda. Kurulum yok, makro yok, VBA yok.**

[![Streamlit](https://img.shields.io/badge/Streamlit-canl%C4%B1%20uygulama-FF4B4B?logo=streamlit&logoColor=white)](https://hakyemezi-filterandsave.streamlit.app)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![Lisans: MIT](https://img.shields.io/badge/lisans-MIT-green)](LICENSE)
[![Diller](https://img.shields.io/badge/aray%C3%BCz-6%20dil-blueviolet)](#diller)

[🇬🇧 English](README.md) · **🇹🇷 Türkçe** · [🇫🇷 Français](README.fr.md) · [🇩🇪 Deutsch](README.de.md) · [🇪🇸 Español](README.es.md) · [🇮🇹 Italiano](README.it.md)

40.000 satırlık bir satış tablonuz ve bir `bölge` sütununuz var; her bölgeye ayrı bir dosya göndermeniz gerekiyor. Excel'de bu bir pivot, bir filtre, bir kopyala, bir yapıştır ve bir kaydet demek — kırk kez. Burada sürükle, tıkla, indir.

**▶️ [Uygulamayı aç](https://hakyemezi-filterandsave.streamlit.app)** — dosyanızı bırakın, üyelik gerekmez.

---

## Neden işinize yarar

**Tek dosya, her değer için ayrı sekme.** Excel'in makro yazmadan yapamadığı şey bu. Kırk ayrı dosya yerine, her biri kendi değerinin adını taşıyan kırk sekmeli tek bir `.xlsx` alırsınız. Sekme adları Excel'in 31 karakter sınırına göre kısaltılır ve çakışmalar otomatik olarak çözülür.

**Aynı anda birden fazla sütuna göre bölme.** `bölge` *ve* `yıl` seçin, her kombinasyon için ayrı bir grup alın — `Marmara - 2024`, `Marmara - 2025` gibi. Bunu elle yapmak bir öğleden sonranızı alır.

**Hiçbir şey üretmeden önce ne alacağınızı görün.** Her grubun satır sayısını gösteren bir tablo; ayrıca grup sayısı, kapsanan satır sayısı, en büyük grup ve kaç satırın atlandığı. Bölme yanlışsa bunu kırk dosyayı açtıktan sonra değil, indirmeden önce fark edersiniz.

**Dışarı çıkmasını istemediğiniz sütunları çıkarın.** Çıktıda hangi sütunların yer alacağını seçin. Kaynak tabloda kurum dışına çıkmaması gereken maliyet veya marj sütunları varsa işinizi görür.

**Sizin dilinizi konuşur.** Arayüzün tamamı İngilizce, Türkçe, Fransızca, Almanca, İspanyolca ve İtalyanca; kenar çubuğunda bayraklarıyla alt alta listelenir. Sayılar da seçtiğiniz dilin biçimine uyar: 1.500 satır İngilizcede 1,500, Fransızcada 1 500 olur.

**Basit scriptleri kıran durumları düşünür.** İçinde `/`, `\`, `:` veya `*` geçen değerler, dosya ya da sekme adına dönüşmeden önce temizlenir. Temizlendiğinde aynı ada düşen iki farklı değer birbirini sessizce ezmek yerine ayrı tutulur. Boş değerler atlanabilir ya da kendi grubu olarak korunabilir. Çok sayfalı çalışma kitaplarında hangi sayfayla çalışacağınızı seçersiniz.

---

## Çıktı seçenekleri

| Seçenek | Elinize geçen | Ne zaman |
|---|---|---|
| **Tek Excel dosyası, her grup ayrı sekmede** | Tek `.xlsx`, her değer için bir sekme | Gruplar arasında gezinmek isteyen birine tek dosya vermek |
| **Zip içinde ayrı Excel dosyaları** | `Marmara.xlsx`, `Ege.xlsx`, … | Her grubu farklı bir kişiye göndermek |
| **Zip içinde ayrı CSV dosyaları** | `Marmara.csv`, `Ege.csv`, … | Başka bir sisteme veri aktarmak ya da çok büyük gruplar |

CSV çıktısı UTF-8 BOM ile yazılır; böylece Türkçe karakterler Excel'de `Ã§` olmak yerine doğru açılır.

---

## Kendi bilgisayarınızda çalıştırma

```bash
git clone https://github.com/hakyemezi/filterandsave.git
cd filterandsave
pip install -r requirements.txt
streamlit run filterandsave.py
```

Python 3.9+ gerekir. Bağımlılıklar `streamlit`, `pandas` ve `openpyxl` — başka bir şey yok.

Her şey bellekte üretilir; sunucunun diskine hiçbir şey yazılmaz ve eşzamanlı kullanıcılar birbirinin dosyasını görmez.

---

## Nasıl kullanılır

1. Bir `.xlsx`, `.csv` veya `.json` dosyası bırakın (200 MB'a kadar).
2. Çalışma kitabında birden fazla sayfa varsa birini seçin.
3. Bölmek istediğiniz sütunu — ya da sütunları — seçin.
4. İsterseniz çıktıda kalacak sütunları belirleyin.
5. Özeti kontrol edin: kaç grup, her biri kaç satır.
6. Çok sekmeli tek dosya mı, ayrı dosyalardan oluşan zip mi seçin.
7. İndirin.

---

## Diller

Arayüz altı dile çevrilmiştir. Altısı da kenar çubuğunda bayraklarıyla birlikte listelenir; ziyaretçi hiçbir menü açmadan kendi dilini görür:

| Dil | Uygulamada | Bu sayfa |
|---|---|---|
| 🇬🇧 **English** | Split a spreadsheet by column | [README.md](README.md) |
| 🇹🇷 **Türkçe** | Tabloyu sütuna göre böl | [README.tr.md](README.tr.md) |
| 🇫🇷 **Français** | Diviser un tableau par colonne | [README.fr.md](README.fr.md) |
| 🇩🇪 **Deutsch** | Tabelle nach Spalte aufteilen | [README.de.md](README.de.md) |
| 🇪🇸 **Español** | Dividir una hoja por columna | [README.es.md](README.es.md) |
| 🇮🇹 **Italiano** | Dividere un foglio per colonna | [README.it.md](README.it.md) |

Çeviriler [`translations.py`](translations.py) dosyasında, her dil için bir sözlük halinde durur. Yeni bir dil eklemek için İngilizce bloğu kopyalayın, değerleri çevirin ve `LANGUAGES` içine bayrağı ve dilin kendine verdiği adı ekleyin. Eksik bıraktığınız anahtarlar İngilizceye düşer, yani yarım bir çeviri bile uygulamayı bozmaz.

Dosya yükleme alanının kendi etiketleri Streamlit'ten gelir ve İngilizce kalır.

---

## Lisans

[MIT](LICENSE)
