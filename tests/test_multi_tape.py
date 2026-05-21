import pytest
from turinglab.multi_tape import MultiTapeTM

def test_multi_tape_init():
    transitions = {
        ("q0", ("1", "1")): ("q_acc", ("0", "0"), ("R", "R"))
    }
    tm = MultiTapeTM(2, ["q0", "q_acc"], ["1"], ["1", "0", "B"], transitions, "q0", ["q_acc"])
    res = tm.run(["1", "1"])
    assert res.accepted
    assert res.final_tapes == ["0", "0"]

def test_multi_tape_reject():
    transitions = {
        ("q0", ("1", "1")): ("q_acc", ("0", "0"), ("R", "R"))
    }
    tm = MultiTapeTM(2, ["q0", "q_acc"], ["1"], ["1", "0", "B"], transitions, "q0", ["q_acc"])
    res = tm.run(["1", "0"])
    assert not res.accepted
    assert res.reason == "no_transition"
