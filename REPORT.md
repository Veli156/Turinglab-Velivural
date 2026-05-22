# TuringLab — Mini Rapor

**Ders:** Hesaplama Kuramı · Bilgisayar Mühendisliği  
**Öğrenci:** Veli Vural  
**Tarih:** Mayıs 2026

---

## 1. Giriş

TuringLab, Turing makinelerini Python'da çalıştıran bir simülasyon kütüphanesidir. Ödev boyunca fark ettiğim şey şu oldu: kağıt üzerinde anlaşılır görünen geçiş kuralları, koda döküldüğünde beklenmedik köşeler çıkarıyor. Özellikle şeridi nasıl temsil edeceğim sorusu başta basit göründü ama Python'da string immutable olduğundan her yazma işlemi yeni bir nesne yaratıyordu — bunu fark edince `dict[int, str]` yapısına geçtim.

---

## 2. Mimari

Proje üç ana katmandan oluşuyor:

**Motor katmanı** (`tm_engine.py`): `SingleTapeTM` sınıfı YAML'dan makine tanımını okuyup `run()` metoduyla simülasyonu yürütür. Şerit sparse dictionary olarak tutulur — bu sayede kafa sola taşsa bile negatif indeks sorunu yaşanmaz. Her adımın anlık görüntüsü `Configuration` dataclass'ı olarak `history` listesine eklenir.

**Makine tanımları** (`machines/`): Dört YAML dosyası. YAML formatını seçmemin sebebi hem okunabilir hem de motordan bağımsız olması — makineyi değiştirmek için koda dokunmak gerekmiyor.

**Test katmanı** (`tests/`): 38 test, her makine için kabul/ret/kenar durum senaryoları.

Önemli tasarım kararları:

| Karar | Tercih | Gerekçe |
|---|---|---|
| Şerit yapısı | `dict[int, str]` | Negatif indeks sorununu önler |
| Blank sembolü | `B` | Görünür karakter, debug kolay |
| History tipi | `Configuration` dataclass | `config.state` gibi erişim |
| NTM tarama | BFS | DFS sonsuz dallarda takılır |

---

## 3. Tasarlanan TM'ler

**TM-1 (Unary → Binary):** Her `1`'i sırayla işaretleyip binary sayacı artırma mantığıyla çalışıyor. Çıktı LSB-first formatında — yani 4 için `001` çıkıyor. Bu tercihi `design_notes.md`'de belirttim.

**TM-2 (Binary Karşılaştırma):** En zorlu makine bu oldu. MSB'den başlayarak her bit çiftini karşılaştırıyorum ama tek şeritte bunu yapmak çok fazla ileri-geri tarama gerektiriyor. Eşit sayılar için ayrı bir `q_check_end` durumu eklemek zorunda kaldım yoksa makine sonsuza gidiyordu. Bu makineyi tasarlarken çok-şeritli TM'nin neden var olduğunu gerçekten anladım.

**TM-3 (Dizgi Kopyalayıcı):** `a` → `X`, `b` → `Y` şeklinde işaretleyip sağa kopyalıyor, sonra geri yükleyerek `w#w` üretiyor. `q_restore` durumunda sola değil sağa ilerleme yazmıştım, verbose modda bakınca fark ettim.

**TM-4 (Parantez Dengesi):** `)` ile başlayan girdiler başta yanlışlıkla kabul ediliyordu. `q0`'da `)` için doğrudan `q_reject` geçişi eklemeyi unutmuştum.

---

## 4. Kavramsal Tartışma

### Modern Bir Programlama Dili ile TM Arasındaki Boşluk

Python ile TM aynı hesaplama gücüne sahip — Church-Turing tezine göre biri yapabiliyorsa diğeri de yapabilir. Ama soyutlama farkı devasa.

Python'da `int(a, 2) > int(b, 2)` yazmak iki saniye sürer. Aynı işi TM'de yapmak için 30'dan fazla geçiş kuralı gerekiyor, O(n²) adım atılıyor. Bu sadece hız farkı değil — TM'de "değişken" yok, "fonksiyon" yok. Her şeyi durum ve şerit üzerinden ifade etmek zorundasın. Bilgiyi taşımanın tek yolu durum olmak.

Bu kısıtlılık aslında bir güç: TM'nin bu kadar sade olması, hangi problemlerin prensipte çözülemez olduğunu kanıtlamayı mümkün kılıyor. Python'un soyutlama katmanları bu sınırları gizler. Durma Problemini Python'da "çözdüm" diyemezsin çünkü argümanın tüm gücü TM'nin minimalliğinden geliyor.

Bu ödevi yaparken fark ettiğim şey şu: TM tasarlamak aslında çok kısıtlı bir ortamda algoritma yazmak. Ve o kısıtlar içinde çalışmak, algoritmanın özünü çok daha net görünür kılıyor.

---

## 5. Sınırlar ve İleri Çalışma

`binary_compare` şu an yalnızca aynı bit uzunluğundaki sayıları doğru karşılaştırıyor — farklı uzunlukta girdi için ön-işlem gerekiyor. Görselleştirici sadece tek şeritli makineleri destekliyor. Bonus C'yi (karşılaştırmalı analiz grafiği) yapmak istedim ama zaman yetmedi.

Bir hafta daha olsaydı: farklı uzunluktaki binary sayılar için `binary_compare`'i genişletirdim ve tek şeritli vs çok şeritli adım sayısı karşılaştırmasını matplotlib ile görselleştirirdim.

---

## 6. Kaynakça

- Sipser, M. (2013). *Introduction to the Theory of Computation* (3rd ed.). Cengage Learning.
- Python 3.13 Dokümantasyonu. https://docs.python.org/3/
- PyYAML Dokümantasyonu. https://pyyaml.org/
- Pytest Dokümantasyonu. https://docs.pytest.org/
