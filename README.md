# TuringLab

**Selçuk Üniversitesi · Bilgisayar Mühendisliği · Hesaplama Kuramı Final Ödevi**  
**Öğrenci:** Veli Vural

Deterministic tek-şeritli Turing makinelerini çalıştıran Python simülasyon kütüphanesi.  
Bonus olarak çok-şeritli TM, non-deterministic TM ve görselleştirici de içerir.

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
38 testin tamamı geçmeli.

### 4. Canlı simülasyonu çalıştır
```bash
python turinglab/demo_run.py
```
`binary_compare` makinesinin `11#10` girdisi üzerinde adım adım çalışmasını gösterir.

---

## Kullanım

```python
from turinglab import SingleTapeTM, RunResult

tm = SingleTapeTM.from_yaml("machines/binary_compare.yaml")
result = tm.run("11#10", max_steps=1000, verbose=True)

print(result.accepted)       # True
print(result.reason)         # 'accept'
print(result.final_tape)     # şerit içeriği
print(result.steps)          # adım sayısı

# Her adım bir Configuration nesnesi
config = result.history[0]
print(config.state)          # 'q0'
print(config.tape)           # '[1]1#10'
print(config.head_position)  # 0
```

---

## Tasarlanan Makineler

| Makine | Açıklama | Kabul koşulu |
|---|---|---|
| `unary_to_binary` | Tekli sayıyı ikiliye çevirir | Her zaman kabul (LSB-first çıktı) |
| `binary_compare` | İki ikili sayıyı karşılaştırır | Sol > Sağ ise kabul |
| `string_copy` | Dizgiyi kopyalar | Her zaman kabul (w → w#w) |
| `student_choice` | Parantez denge kontrolü | Dengeli ise kabul |

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
│   ├── multi_tape.py      # Bonus A: çok-şeritli motor
│   ├── ntm.py             # Bonus B: non-deterministic motor
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
