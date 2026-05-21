# TuringLab — Mini Rapor

**Ders:** Otomata
**Öğrenci:** [Veli Vural]  
**Tarih:** Mayıs 2026  

---

## 1. Giriş

TuringLab, deterministic tek-şeritli Turing makinelerini (ve bonus olarak çok-şeritli ile non-deterministic varyantlarını) Python'da çalıştıran bir simülasyon kütüphanesidir. Proje; bir TM motorunu sıfırdan yazmayı, bu motorla somut problemleri çözmeyi ve hesaplama kuramının soyut kavramlarını elle tutulan bir artefakta dönüştürmeyi hedefler.

---

## 2. Mimari

Proje `turinglab/` paketi altında organize edilmiştir:

- **`tm_engine.py`** — Çekirdeği oluşturur. `SingleTapeTM` sınıfı YAML'dan TM yükler ve `run()` metoduyla simülasyonu yürütür. Şerit dahili olarak `dict[int, str]` (sparse representation) ile tutulur; bu sayede hem sol hem sağ sonsuz genişleyebilir ve Python'un negatif indeks sorununu ortadan kaldırır. Her adımın anlık görüntüsü `Configuration` dataclass'ı olarak `history` listesine eklenir; bu, `result.history[i].state` gibi attribute erişimine olanak tanır.

- **`multi_tape.py`** (Bonus A) — `MultiTapeTM` sınıfı, YAML'da `k` ile belirtilen şerit sayısını destekler. Her şerit bağımsız bir sparse dict olarak tutulur.

- **`ntm.py`** (Bonus B) — `NondeterministicTM`, BFS (genişlik öncelikli arama) ile hesaplama ağacını gezdiğinden sonsuz dallara takılmaz; `max_depth` ve `max_branches` parametreleriyle kontrol altında tutulur.

- **`visualizer.py`** (Bonus D) — Pillow ile her adım için PNG karesi, imageio ile GIF üretir.

**Önemli tasarım kararları:**

| Karar | Tercih | Gerekçe |
|---|---|---|
| Şerit yapısı | `dict[int, str]` | Negatif indeks sorununu önler, sparse erişim O(1) |
| Blank sembolü | `"B"` | Görünür karakter; debug kolaylığı |
| History tipi | `Configuration` dataclass | `config.state` gibi attribute erişimi mümkün |
| NTM tarama | BFS | DFS sonsuz dallarda takılır |

---

## 3. Tasarlanan TM'ler

**TM-1 — Unary → Binary Çevirici:** Her `1`'i işaretleyip (X) binary sayacı artırma döngüsü kurar. Çıktı LSB-first (en az anlamlı bit solda) formatındadır; bu tercih `design_notes.md`'de belirtilmiştir. Girdi uzunluğu n için O(n²) adım gerekir.

**TM-2 — İkili Karşılaştırma:** MSB'den başlayarak her bit çifti işaretlenerek karşılaştırılır. Sol > sağ ise kabul, aksi hâlde reddeder. Tek şeritte ileri-geri tarama O(n²) adım gerektirir; bu, çok-şeritli TM'nin motivasyonunu doğal olarak ortaya koyar.

**TM-3 — Dizgi Kopyalayıcı:** `a` → X, `b` → Y şeklinde işaretleme yaparak karakterleri sağdaki kopyaya aktarır; ardından X/Y'leri orijinal sembollere geri yükler. `w#w` çıktısını üretir. O(n²) adım.

**TM-4 — Parantez Denge Kontrolü:** Her `(` için en yakın eşleşmemiş `)` bulunur; eşleşen çiftler X/Y ile işaretlenir. Tüm karakterler işaretlendiyse kabul, aksi reddeder. Bu makine en ilginç kenar durumları barındırır: `)` ile başlayan girdi, tek karakter, iç içe parantezler.

**En zorlayıcı:** TM-2 — Tek şeritte bitwise karşılaştırma için gereken ileri-geri tarama sayısı ve `q_check_end` durumuyla eşitlik durumunun ayrı ele alınması beklenenden karmaşık çıktı.

---

## 4. Kavramsal Tartışma

### (c) Modern Bir Programlama Dili ile TM Arasındaki Boşluk

Turing makinesi ve Python hesaplama gücü açısından eşdeğerdir (Church-Turing tezi); Python'da hesaplanabilen her şey bir TM ile de hesaplanabilir, tersi de doğrudur. Ancak **soyutlama düzeyi** arasındaki uçurum derindir.

Python, veri yapıları (liste, sözlük, küme), yüksek seviyeli kontrol akışı (döngüler, istisnalar, üretecler), modül sistemi ve dinamik tip denetimi sunar. Programcı "ne yapılacağını" tanımlar; yorumlayıcı "nasıl yapılacağını" yönetir. TM ise yalnızca beş bileşenden oluşur: durum kümesi, alfabe, geçiş fonksiyonu, başlangıç durumu, kabul durumları. Her adımda yalnızca bir sembol okunur, bir sembol yazılır, kafa bir adım kayar.

Bu boşluğun pratik yansıması TuringLab'da açıkça görülür: Python'da üç satırla yazılabilen "ikili sayıyı bir artır" işlemi, TM'de sekiz geçiş kuralı gerektirir. `binary_compare` TM'i, Python'un iki satırlık `int(a, 2) > int(b, 2)` karşılaştırmasını 30'dan fazla geçiş kuralına indirger.

Boşluk, **zaman ve alan karmaşıklığında** da kendini gösterir: Python'da O(1) olan bir sözlük erişimi, TM'de O(n) ileri-geri taramaya dönüşebilir. Bununla birlikte bu kısıtlılık bir zayıflık değil, teorik analizin gücüdür: TM'nin minimalist yapısı, hangi problemlerin prensipte çözülemez olduğunu (Durma Problemi gibi) kanıtlamayı mümkün kılar; oysa Python'un soyutlama katmanları bu sınırları gizler.

---

## 5. Sınırlar ve İleri Çalışma

**Mevcut sınırlar:**

- Görselleştirici (`visualizer.py`) yalnızca tek-şeritli TM'leri destekler; multi-tape için genişletilmedi.
- `binary_compare` yalnızca aynı bit uzunluğundaki sayıları doğru karşılaştırır; farklı uzunlukta girdiler için ek ön-işlem gerekir.
- NTM testi yalnızca basit bir örnek içeriyor; daha kapsamlı NTM makineleri tasarlanabilir.

**Bir hafta daha olsaydı:**

- Bonus C tamamlanarak tek-şeritli, çok-şeritli ve NTM arasında adım sayısı karşılaştırması yapılacak ve matplotlib grafiği eklenecekti.
- `binary_compare` farklı uzunluktaki girdileri de doğru işleyecek şekilde genişletilecekti.
- Web tabanlı interaktif bir görselleştirici (adım adım ileri/geri) eklenebilirdi.

---

## 6. Kaynakça

- Sipser, M. (2013). *Introduction to the Theory of Computation* (3rd ed.). Cengage Learning.
- Python Software Foundation. *Python 3.12 Documentation*. https://docs.python.org/3/
- PyYAML Documentation. https://pyyaml.org/wiki/PyYAMLDocumentation
- Pytest Documentation. https://docs.pytest.org/
