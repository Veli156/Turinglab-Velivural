import sys
import os

# Üst klasörü arama yoluna ekleme
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from turinglab.tm_engine import SingleTapeTM

try:
    tm = SingleTapeTM.from_yaml(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "machines", "binary_compare.yaml"))
    
    print("\n--- Turing Makinesi Canlı Simülasyonu Başlıyor ---")
    
    result = tm.run(input_string="11#10", max_steps=1000, verbose=True)
    
    print("\n--- SİMÜLASYON SONUCU ---")
    print(f"Kabul Edildi mi?: {result.accepted} (Neden: {result.reason})")
    print(f"Şeridin Son Hali: {result.final_tape}")
    print(f"Toplam Adım Sayısı: {result.steps}")

except Exception as e:
    print(f"Bir hata oluştu: {e}")
