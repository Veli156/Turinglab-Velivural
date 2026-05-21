"""
Bölüm 1 — TM Motoru testleri (test_tm_engine.py)
En az 8 test fonksiyonu zorunludur.
"""
import pytest
import sys
from io import StringIO
from turinglab import SingleTapeTM, RunResult, Configuration


# ---------------------------------------------------------------------------
# Fixture: basit tek geçişli TM
# ---------------------------------------------------------------------------
@pytest.fixture
def simple_tm():
    """'1' girdisini '0' yapıp kabul eden minimal TM."""
    transitions = {
        ("q0", "1"): ("q1", "0", "R"),
        ("q1", "B"): ("q_acc", "B", "L"),
    }
    return SingleTapeTM(
        states=["q0", "q1", "q_acc", "q_rej"],
        input_alphabet=["1"],
        tape_alphabet=["1", "0", "B"],
        transitions=transitions,
        start_state="q0",
        accept_states=["q_acc"],
        reject_states=["q_rej"],
    )


# ---------------------------------------------------------------------------
# Test 1: Başlangıç parametreleri doğru atanıyor mu?
# ---------------------------------------------------------------------------
def test_init(simple_tm):
    assert simple_tm.start_state == "q0"
    assert "q_acc" in simple_tm.accept_states
    assert "q_rej" in simple_tm.reject_states


# ---------------------------------------------------------------------------
# Test 2: Kabul durumu
# ---------------------------------------------------------------------------
def test_run_accept(simple_tm):
    res = simple_tm.run("1")
    assert res.accepted is True
    assert res.reason == "accept"
    assert res.final_tape == "0"


# ---------------------------------------------------------------------------
# Test 3: no_transition durumu
# ---------------------------------------------------------------------------
def test_run_no_transition(simple_tm):
    res = simple_tm.run("0")
    assert res.accepted is False
    assert res.reason == "no_transition"


# ---------------------------------------------------------------------------
# Test 4: reject_states'e ulaşınca doğru dönüş
# ---------------------------------------------------------------------------
def test_run_explicit_reject():
    """Açık reject durumuna sahip TM testi."""
    transitions = {
        ("q0", "0"): ("q_rej", "0", "R"),
        ("q0", "1"): ("q_acc", "1", "R"),
    }
    tm = SingleTapeTM(
        states=["q0", "q_acc", "q_rej"],
        input_alphabet=["0", "1"],
        tape_alphabet=["0", "1", "B"],
        transitions=transitions,
        start_state="q0",
        accept_states=["q_acc"],
        reject_states=["q_rej"],
    )
    res = tm.run("0")
    assert res.accepted is False
    assert res.reason == "reject"


# ---------------------------------------------------------------------------
# Test 5: Timeout durumu
# ---------------------------------------------------------------------------
def test_timeout():
    transitions = {
        ("q0", "1"): ("q0", "1", "R"),
        ("q0", "B"): ("q0", "B", "R"),
    }
    tm = SingleTapeTM(["q0"], ["1"], ["1", "B"], transitions, "q0", ["q_acc"])
    res = tm.run("111", max_steps=5)
    assert res.accepted is False
    assert res.reason == "timeout"
    assert res.steps == 5


# ---------------------------------------------------------------------------
# Test 6: verbose=True çıktı formatı şartnameye uygun mu?
# ---------------------------------------------------------------------------
def test_verbose_output(simple_tm):
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    simple_tm.run("1", verbose=True)
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    assert "Adım 0" in output
    assert "Durum: q0" in output
    assert "Hareket: R" in output
    assert "Şerit:" in output


# ---------------------------------------------------------------------------
# Test 7: Hatalı YAML → ValueError
# ---------------------------------------------------------------------------
def test_invalid_yaml(tmp_path):
    p = tmp_path / "invalid.yaml"
    p.write_text("invalid: yaml: :")
    with pytest.raises(ValueError, match="YAML okuma hatası"):
        SingleTapeTM.from_yaml(str(p))


# ---------------------------------------------------------------------------
# Test 8: Eksik zorunlu alan → ValueError
# ---------------------------------------------------------------------------
def test_missing_keys_yaml(tmp_path):
    p = tmp_path / "missing.yaml"
    p.write_text("states: [q0]\n")
    with pytest.raises(ValueError, match="Eksik anahtar"):
        SingleTapeTM.from_yaml(str(p))


# ---------------------------------------------------------------------------
# Test 9: history her adımı Configuration nesnesi olarak kaydediyor mu?
# ---------------------------------------------------------------------------
def test_history_configuration_objects(simple_tm):
    """history listesindeki her eleman Configuration dataclass'ı olmalı."""
    res = simple_tm.run("1")
    assert len(res.history) >= 1
    config = res.history[0]
    # Ödevin istediği attribute erişimi
    assert hasattr(config, "state")
    assert hasattr(config, "tape")
    assert hasattr(config, "head_position")
    assert config.state == "q0"
    assert config.head_position == 0
    assert isinstance(config, Configuration)


# ---------------------------------------------------------------------------
# Test 10: Boş girdi → makine çökmemeli
# ---------------------------------------------------------------------------
def test_empty_input(simple_tm):
    res = simple_tm.run("")
    # Boş girdi: q0 durumunda B okur, geçiş yok → no_transition
    assert res.accepted is False
    assert res.reason == "no_transition"
