import pytest
from turinglab.ntm import NondeterministicTM

def test_ntm_accept():
    transitions = {
        ("q0", "0"): [
            ("q0", "0", "R"),
            ("q0", "0", "L")
        ],
        ("q0", "1"): [
            ("q_acc", "1", "R")
        ]
    }
    tm = NondeterministicTM(["q0", "q_acc"], ["0", "1"], ["0", "1", "B"], transitions, "q0", ["q_acc"])
    
    res = tm.run("001")
    assert res.accepted
    assert len(res.accepting_paths) > 0

def test_ntm_reject():
    transitions = {
        ("q0", "0"): [("q0", "0", "R")]
    }
    tm = NondeterministicTM(["q0", "q_acc"], ["0"], ["0", "B"], transitions, "q0", ["q_acc"])
    res = tm.run("000", max_depth=5)
    assert not res.accepted
