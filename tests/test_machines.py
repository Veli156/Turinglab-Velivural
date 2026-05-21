"""
Bölüm 2 — 4 TM Tasarımı testleri (test_machines.py)
Her TM için en az 5 test: 2 kabul, 2 ret, 1 kenar durum.
"""
import pytest
import os
from turinglab import SingleTapeTM

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MACHINES_DIR = os.path.join(BASE_DIR, "machines")


def get_machine(name):
    """Makineleri MACHINES_DIR'den yükleyen yardımcı fonksiyon."""
    return SingleTapeTM.from_yaml(os.path.join(MACHINES_DIR, name))


# ---------------------------------------------------------------------------
# TM-1: Unary → Binary Çevirici
# Çıktı LSB-first (en düşük anlamlı bit solda) formatındadır.
# ---------------------------------------------------------------------------
class TestUnaryToBinary:
    def test_one(self):
        """1 (unary) → '1' (binary LSB-first)"""
        tm = get_machine("unary_to_binary.yaml")
        assert tm.run("1", max_steps=5000).final_tape == "1"

    def test_two(self):
        """11 (unary=2) → '01' (binary LSB-first: 010 → 2)"""
        tm = get_machine("unary_to_binary.yaml")
        assert tm.run("11", max_steps=5000).final_tape == "01"

    def test_three(self):
        """111 (unary=3) → '11' (binary LSB-first: 11 → 3)"""
        tm = get_machine("unary_to_binary.yaml")
        assert tm.run("111", max_steps=5000).final_tape == "11"

    def test_four(self):
        """1111 (unary=4) → '001' (binary LSB-first: 001 → 4)"""
        tm = get_machine("unary_to_binary.yaml")
        assert tm.run("1111", max_steps=5000).final_tape == "001"

    def test_five(self):
        """11111 (unary=5) → '101' (binary LSB-first: 101 → 5)"""
        tm = get_machine("unary_to_binary.yaml")
        assert tm.run("11111", max_steps=5000).final_tape == "101"

    def test_single_char_edge(self):
        """Tek karakterli girdi kenar durumu: 1 → kabul edilmeli"""
        tm = get_machine("unary_to_binary.yaml")
        res = tm.run("1", max_steps=5000)
        assert res.accepted is True


# ---------------------------------------------------------------------------
# TM-2: İki İkili Sayıyı Karşılaştıran TM
# Kabul: sol > sağ  |  Ret: sol <= sağ
# ---------------------------------------------------------------------------
class TestBinaryCompare:
    def test_left_greater_simple(self):
        """10 > 01 → kabul"""
        tm = get_machine("binary_compare.yaml")
        assert tm.run("10#01", max_steps=5000).accepted is True

    def test_left_greater_multi(self):
        """11 > 10 → kabul"""
        tm = get_machine("binary_compare.yaml")
        assert tm.run("11#10", max_steps=5000).accepted is True

    def test_left_less(self):
        """01 < 10 → ret"""
        tm = get_machine("binary_compare.yaml")
        assert tm.run("01#10", max_steps=5000).accepted is False

    def test_equal(self):
        """11 == 11 → ret (eşit, büyük değil)"""
        tm = get_machine("binary_compare.yaml")
        assert tm.run("11#11", max_steps=5000).accepted is False

    def test_zero_vs_one(self):
        """00 < 01 → ret"""
        tm = get_machine("binary_compare.yaml")
        assert tm.run("00#01", max_steps=5000).accepted is False

    def test_pdf_example(self):
        """Ödev PDF örneği: 1011 < 1100 → ret"""
        tm = get_machine("binary_compare.yaml")
        assert tm.run("1011#1100", max_steps=5000).accepted is False


# ---------------------------------------------------------------------------
# TM-3: Dizgi Kopyalayıcı
# Girdi: w  →  Çıktı: w#w
# ---------------------------------------------------------------------------
class TestStringCopy:
    def test_single_a(self):
        tm = get_machine("string_copy.yaml")
        assert tm.run("a", max_steps=5000).final_tape == "a#a"

    def test_ab(self):
        tm = get_machine("string_copy.yaml")
        assert tm.run("ab", max_steps=5000).final_tape == "ab#ab"

    def test_abba(self):
        tm = get_machine("string_copy.yaml")
        assert tm.run("abba", max_steps=5000).final_tape == "abba#abba"

    def test_single_b(self):
        tm = get_machine("string_copy.yaml")
        assert tm.run("b", max_steps=5000).final_tape == "b#b"

    def test_longer(self):
        tm = get_machine("string_copy.yaml")
        assert tm.run("bab", max_steps=5000).final_tape == "bab#bab"

    def test_all_a(self):
        """Kenar durum: tek tip karakterden oluşan dizi"""
        tm = get_machine("string_copy.yaml")
        assert tm.run("aaa", max_steps=5000).final_tape == "aaa#aaa"


# ---------------------------------------------------------------------------
# TM-4: Öğrenci Seçimi — Parantez Denge Kontrolü
# Kabul: dengeli  |  Ret: dengesiz
# ---------------------------------------------------------------------------
class TestStudentChoice:
    def test_simple_balanced(self):
        """() → kabul"""
        tm = get_machine("student_choice.yaml")
        assert tm.run("()", max_steps=5000).accepted is True

    def test_nested_balanced(self):
        """(()()) → kabul"""
        tm = get_machine("student_choice.yaml")
        assert tm.run("(()())", max_steps=5000).accepted is True

    def test_unbalanced_open(self):
        """(() → ret (kapatılmamış parantez)"""
        tm = get_machine("student_choice.yaml")
        assert tm.run("(()", max_steps=5000).accepted is False

    def test_wrong_order(self):
        """)( → ret (önce kapanış)"""
        tm = get_machine("student_choice.yaml")
        assert tm.run(")(", max_steps=5000).accepted is False

    def test_deeply_nested(self):
        """((())) → kabul"""
        tm = get_machine("student_choice.yaml")
        assert tm.run("((()))", max_steps=5000).accepted is True

    def test_single_open(self):
        """Kenar durum: tek açık parantez → ret"""
        tm = get_machine("student_choice.yaml")
        assert tm.run("(", max_steps=5000).accepted is False
