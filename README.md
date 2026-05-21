# TuringLab

**Selçuk Üniversitesi · Bilgisayar Mühendisliği · Hesaplama Kuramı Final Ödevi**  
**Öğrenci:** [Adınız Soyadınız]

Deterministic tek-şeritli Turing makinelerini çalıştıran Python simülasyon kütüphanesi.  
Bonus olarak çok-şeritli TM, non-deterministic TM ve görselleştirici de içerir.

---

## Kurulum

```bash
git clone https://github.com/kullanici-adi/turinglab-adsoyad.git
cd turinglab-adsoyad
pip install -r requirements.txt
```

## Kullanım

```python
from turinglab import SingleTapeTM, RunResult

# YAML dosyasından TM yükle
tm = SingleTapeTM.from_yaml("machines/binary_compare.yaml")

# Çalıştır
result = tm.run("11#10", max_steps=1000, verbose=False)

print(result.accepted)     # True
print(result.reason)       # 'accept'
print(result.final_tape)   # şerit içeriği
print(result.steps)        # adım sayısı

# Tarihçe — her adım bir Configuration nesnesi
config = result.history[0]
print(config.state)         # 'q0'
print(config.tape)          # '[1]1#10'
print(config.head_position) # 0
```

### Verbose mod

```python
tm.run("11#10", verbose=True)
# Adım 0 | Durum: q0 | Şerit: [1]1#10 | Hareket: R
# Adım 1 | Durum: q0 | Şerit: 1[1]#10 | Hareket: R
# ...
```

### Multi-tape (Bonus A)

```python
from turinglab import MultiTapeTM
tm = MultiTapeTM.from_yaml("machines/multi_tape_example.yaml")
result = tm.run(["101", "110"])
print(result.final_tapes)
```

### Non-deterministic TM (Bonus B)

```python
from turinglab import NondeterministicTM
# NTM manuel oluşturma
result = tm.run("001", max_depth=100, max_branches=10000)
print(result.accepted)
print(result.accepting_paths)
```

## Testleri Çalıştırma

```bash
cd turinglab
pytest tests/ -v
```

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

## Tasarlanan Makineler

| Makine | Açıklama | Kabul koşulu |
|---|---|---|
| `unary_to_binary` | Tekli sayıyı ikiliye çevirir | Her zaman kabul (LSB-first çıktı) |
| `binary_compare` | İki ikili sayıyı karşılaştırır | Sol > Sağ ise kabul |
| `string_copy` | Dizgiyi kopyalar | Her zaman kabul (w → w#w) |
| `student_choice` | Parantez denge kontrolü | Dengeli ise kabul |
