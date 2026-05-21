"""
Bonus A: Çok Şeritli TM Motoru (MultiTapeTM)
"""
import yaml
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class MultiRunResult:
    accepted: bool
    reason: str
    final_tapes: List[str]
    steps: int
    history: list[dict]

class MultiTapeTM:
    def __init__(self, k: int, states: List[str], input_alphabet: List[str], tape_alphabet: List[str],
                 transitions: Dict, start_state: str, accept_states: List[str], reject_states: List[str] = None):
        self.k = k
        self.states = states
        self.input_alphabet = input_alphabet
        self.tape_alphabet = tape_alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
        self.reject_states = reject_states or []
        self.blank_symbol = "B"
        
    @classmethod
    def from_yaml(cls, file_path: str) -> "MultiTapeTM":
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception as e:
            raise ValueError(f"YAML okuma hatası: {e}")
            
        k = data.get("k", 1)
        required_keys = ["states", "input_alphabet", "tape_alphabet", "transitions", "start_state", "accept_states"]
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Eksik anahtar: {key}")
                
        trans_dict = {}
        for tr in data["transitions"]:
            read_tuple = tuple(str(x) for x in tr["read"])
            write_tuple = tuple(str(x) for x in tr["write"])
            move_tuple = tuple(tr["move"])
            
            if len(read_tuple) != k or len(write_tuple) != k or len(move_tuple) != k:
                 raise ValueError("Kural listeleri k uzunluğunda olmalı.")
                 
            trans_dict[(tr["state"], read_tuple)] = (tr["next"], write_tuple, move_tuple)
            
        return cls(
            k=k,
            states=data["states"],
            input_alphabet=[str(x) for x in data["input_alphabet"]],
            tape_alphabet=[str(x) for x in data["tape_alphabet"]],
            transitions=trans_dict,
            start_state=data["start_state"],
            accept_states=data["accept_states"],
            reject_states=data.get("reject_states", [])
        )
        
    def _clean_tape_string(self, tape: dict[int, str]) -> str:
        if not tape:
            return ""
        min_pos = min(tape.keys())
        max_pos = max(tape.keys())
        res = ""
        for i in range(min_pos, max_pos + 1):
            res += tape.get(i, self.blank_symbol)
        return res.strip(self.blank_symbol)
        
    def run(self, input_strings: List[str], max_steps: int = 1000) -> MultiRunResult:
        if len(input_strings) != self.k:
            raise ValueError(f"input_strings uzunluğu {self.k} olmalıdır.")
            
        tapes = [{i: char for i, char in enumerate(inp)} if inp else {0: self.blank_symbol} for inp in input_strings]
        heads = [0] * self.k
        current_state = self.start_state
        steps = 0
        history = []
        
        while steps < max_steps:
            current_chars = tuple(tape.get(head, self.blank_symbol) for tape, head in zip(tapes, heads))
            
            history.append({
                "step": steps,
                "state": current_state,
                "tapes": [t.copy() for t in tapes],
                "heads": list(heads)
            })
            
            if current_state in self.accept_states:
                return MultiRunResult(True, "accept", [self._clean_tape_string(t) for t in tapes], steps, history)
            if current_state in self.reject_states:
                 return MultiRunResult(False, "reject", [self._clean_tape_string(t) for t in tapes], steps, history)
                 
            trans = self.transitions.get((current_state, current_chars))
            if not trans:
                return MultiRunResult(False, "no_transition", [self._clean_tape_string(t) for t in tapes], steps, history)
                
            next_state, write_chars, moves = trans
            
            for i in range(self.k):
                tapes[i][heads[i]] = write_chars[i]
                if moves[i] == "R":
                    heads[i] += 1
                elif moves[i] == "L":
                    heads[i] -= 1
                    
            current_state = next_state
            steps += 1
            
        return MultiRunResult(False, "timeout", [self._clean_tape_string(t) for t in tapes], steps, history)

    @classmethod
    def get_binary_adder_example(cls):
        """
        3-şeritli ikili toplama makinesi mantığı (LSB başta):
        Şerit 1: Birinci sayı (örn. 101)
        Şerit 2: İkinci sayı (örn. 110)
        Şerit 3: Sonuç yazılacak
        Durumlar: q0 (elde 0), q1 (elde 1)
        Geçiş örnekleri:
        (q0, ('1', '1', 'B')) -> (q1, ('1', '1', '0'), ('R', 'R', 'R'))  # 1+1 = 0, elde 1
        (q1, ('1', '1', 'B')) -> (q1, ('1', '1', '1'), ('R', 'R', 'R'))  # 1+1+1 = 1, elde 1
        (q0, ('1', '0', 'B')) -> (q0, ('1', '0', '1'), ('R', 'R', 'R'))  # 1+0 = 1, elde 0
        """
        pass
