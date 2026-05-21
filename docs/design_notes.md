# Tasarım Notları — TuringLab Bölüm 2

## TM-1: Unary → Binary Çevirici (`unary_to_binary.yaml`)

**1. Strateji:** Şerit üzerindeki her `1` sembolü sırayla `X` ile işaretlenir. Her işaretleme turunda binary sayaç (şeridin sağ tarafına, `#` ayracından sonra yazılmış) bir artırılır. Tüm `1`'ler işaretlendiğinde `X` ve `#` temizlenip yalnızca binary sayı bırakılır.

**2. Durum sayısı:** 6 durum kullanıldı: `q0` (1 bul ve işaretle), `q_find_hash` (# konumuna git), `q_inc` (binary artır), `q_back` (başa dön), `q_clean` (temizle), `q_accept`. Daha az durum teorik olarak mümkün olabilir ancak `q_back` ile `q_clean`'i birleştirmek geçiş kurallarını belirsizleştirir.

**3. Şerit alfabesi:** `{1, 0, B, X, #}`. `X` işaretleyici olarak seçildi çünkü input alfabesiyle çakışmaz. `#` ayraç olarak binary bölümü unary bölümden ayırır. Alternatif olarak iki ayrı işaretleyici yerine tek bir `X` yeterli oldu.

**4. Karmaşıklık:** n uzunluğunda unary girdi için her tur ortalama n/2 adım ileri + binary artırım (~log n) + geri dönüş (~n) atar. Toplam O(n²) adım. Binary sayının uzunluğu log n olduğundan artırım kısmı dominant değil.

**5. Hata ayıklama hikayesi:** İlk sürümde `q_inc` durumunda carry-over geçişi eksikti; `1`'ler üzerinde sağa giderken yeni pozisyona `B` yerine `0` yazılması gerektiği atlandı. Bu yüzden `11` (2) için `01` yerine `11` çıktı alındı. `verbose=True` modu ile adım adım inceleyince `q_inc` durumunun `1` okuyunca sağa ilerlemediği fark edildi.

---

## TM-2: İkili Sayıları Karşılaştıran TM (`binary_compare.yaml`)

**1. Strateji:** MSB'den (en anlamlı bit) başlayarak her bit `X` ile işaretlenir, `#` geçilip karşı taraftaki aynı konumdaki bit bulunur. Sol bit `0`, sağ bit `1` ise direkt reddedilir. Sol bit `1`, sağ bit `0` ise direkt kabul edilir. Eşit bitse sonraki bite geçilir. Tüm bitler işaretlenip eşitlik kalırsa ret.

**2. Durum sayısı:** 9 durum: `q0`, `q_find_0`, `q_cmp_0`, `q_find_1`, `q_cmp_1`, `q_back`, `q_check_end`, `q_accept`, `q_reject`. `q_find_0`/`q_find_1` ayrımı zorunlu; okunan biti hatırlamak için ayrı bir durum kullanmak gerekti çünkü TM'de "değişken" yok, durum bilgiyi taşımalı.

**3. Şerit alfabesi:** `{0, 1, X, #, B}`. `X` işaretleyici olarak her iki tarafta da kullanıldı. Alternatif olarak sol taraf için `X`, sağ taraf için `Y` ayrımı yapılabilirdi ama tek `X` yeterli oldu.

**4. Karmaşıklık:** n bitlik sayılar için her bit karşılaştırması ~3n adım (sol işaretle, # geç, sağ bul, geri dön). Toplam O(n²) adım. Çok-şeritli TM'de bu O(n)'e düşer — TM-2 bu motivasyonun somut örneğidir.

**5. Hata ayıklama hikayesi:** `q_check_end` durumu başta yoktu; eşit sayılar için `q_back` durumu sonsuza takılıyordu. Tüm bitler işaretlenince `#` ile karşılaşıldığında ne yapılacağı tanımlı değildi. `q_check_end` eklenerek `#` sonrasında yalnızca `X`'ler varsa ret verilmesi sağlandı.

---

## TM-3: Dizgi Kopyalayıcı (`string_copy.yaml`)

**1. Strateji:** Soldaki her karakter sırayla okunur, `X` (a için) veya `Y` (b için) ile işaretlenir, şeridin en sağına gidilerek kopyası yazılır, ardından başa dönülür. Tüm karakterler işaretlenip `#` ile karşılaşıldığında `X`→`a`, `Y`→`b` dönüşümüyle orijinal geri yüklenir.

**2. Durum sayısı:** 8 durum. `q_copy_a` ve `q_copy_b` ayrı durumlar gerektirir çünkü hangi karakteri kopyalayacağını hatırlamak zorunda. Birleştirme mümkün değil.

**3. Şerit alfabesi:** `{a, b, X, Y, #, B}`. `X` → a işaretleyici, `Y` → b işaretleyici. `#` ayraç; orijinal ile kopya arasında. Alternatif: yalnızca tek bir işaretleyici ile ve iki geçiş yapılabilir ama bu durumu sayısını artırır.

**4. Karmaşıklık:** n uzunluğunda girdi için her karakter kopyalaması ~2n + kopya_uzunluğu adım atar. Toplam O(n²) adım.

**5. Hata ayıklama hikayesi:** `q_restore` durumunda `X`→`a`, `Y`→`b` dönüşümü yapılırken sola doğru ilerleme unutulmuştu; sağa ilerleme yazılmıştı. Bu yüzden restore işlemi sonsuz döngüye girdi. `verbose=True` ile birkaç adım bakıldığında kafa yönünün yanlış olduğu görüldü.

---

## TM-4: Parantez Denge Kontrolü (`student_choice.yaml`)

**1. Strateji:** En soldaki işaretlenmemiş `(` bulunur, `X` ile işaretlenir. Sağa gidilerek en yakın işaretlenmemiş `)` bulunur, `Y` ile işaretlenir. Eşleşme yoksa (sağa gidince blank'a ulaşıldı) reddedilir. Tüm karakterler işaretlenince şerit başından `(` veya `)` kaldı mı kontrol edilir; yoksa kabul, varsa reddedilir.

**2. Durum sayısı:** 6 durum: `q0`, `q_find_close`, `q_back`, `q_check_all_x`, `q_accept`, `q_reject`. Minimal sayıda tutuldu; `q_back` ile `q_check_all_x` birleştirilemiyor çünkü farklı tetikleyicileri var.

**3. Şerit alfabesi:** `{(, ), X, Y, B}`. `X` açık, `Y` kapalı parantez işaretleyicisi. Alternatif olarak her ikisi için `X` kullanılabilirdi ama `q_check_all_x` durumunda `)` ile `Y`'yi ayırt etmek gerekirdi.

**4. Karmaşıklık:** n parantez için her eşleştirme ~n adım. Toplam O(n²) adım.

**5. Hata ayıklama hikayesi:** `)` ile başlayan `)(` girdisi başta yanlışlıkla kabul ediliyordu. `q0` durumunda `)` okunduğunda doğrudan `q_reject`'e geçiş eklenmemişti; bunun yerine `q_find_close`'a gidiyordu ve orada `X`'i bulunca `q_back`'e geçiyordu. `q0`'da `)` için açık `q_reject` geçişi eklenince düzeldi.
