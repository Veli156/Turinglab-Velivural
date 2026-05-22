# TuringLab

**Selçuk Üniversitesi · Bilgisayar Mühendisliği · Hesaplama Kuramı Final Ödevi**  
**Öğrenci:** Veli Vural

Turing makinelerini Python'da simüle eden bir kütüphane. Tek şeritli deterministik TM'den başlayıp çok şeritli, non-deterministik ve görselleştirici bonus'larına kadar uzanıyor.

---

## Kurulum ve Çalıştırma

### 1. Repoyu klonla
```bash
git clone https://github.com/Veli156/Turinglab-Velivural.git
cd Turinglab-Velivural
```

### 2. Bağımlılıkları yükle
```bash
pip install pyyaml pytest pillow imageio
```

### 3. Testleri çalıştır
```bash
python -m pytest tests/ -v
```

### 4. Canlı demo
```bash
python turinglab/demo_run.py
```
`binary_compare` makinesinin `11#10` girdisi üzerinde adım adım nasıl çalıştığını gösterir.

---

## Kullanım

```python
from turinglab import SingleTapeTM

tm = SingleTapeTM.from_yaml("machines/binary_compare.yaml")
result = tm.run("11#10", max_steps=1000, verbose=True)

print(result.accepted)       # True
print(result.reason)         # 'accept'
print(result.final_tape)     # şerit içeriği
print(result.steps)          # adım sayısı

config = result.history[0]
print(config.state)          # 'q0'
print(config.tape)           # '[1]1#10'
print(config.head_position)  # 0
```

---

## Tasarlanan Makineler

| Makine | Ne yapar | Ne zaman kabul eder |
|---|---|---|
| `unary_to_binary` | Tekli sayıyı ikiliye çevirir | Her zaman (LSB-first çıktı verir) |
| `binary_compare` | İki ikili sayıyı karşılaştırır | Sol > Sağ ise |
| `string_copy` | Girdiyi kopyalar | Her zaman (w → w#w) |
| `student_choice` | Parantez dengesi kontrol eder | Dengeli ise |

En zorlu olan `binary_compare` oldu — tek şeritte bit bit karşılaştırma yapmak düşündüğümden çok daha fazla ileri-geri tarama gerektirdi. `q_check_end` durumunu sonradan eklemek zorunda kaldım, yoksa eşit sayılarda makine sonsuza gidiyordu.

---

## Proje Yapısı

```
turinglab/
├── README.md
├── REPORT.md
├── requirements.txt
├── .gitignore
├── turinglab/
│   ├── __init__.py
│   ├── tm_engine.py       # Bölüm 1: TM motoru
│   ├── multi_tape.py      # Bonus A: çok şeritli
│   ├── ntm.py             # Bonus B: non-deterministik
│   └── visualizer.py      # Bonus D: görselleştirme
├── machines/
│   ├── unary_to_binary.yaml
│   ├── binary_compare.yaml
│   ├── string_copy.yaml
│   └── student_choice.yaml
├── tests/
│   ├── test_tm_engine.py
│   ├── test_machines.py
│   ├── test_multi_tape.py
│   └── test_ntm.py
└── docs/
    └── design_notes.md
```
