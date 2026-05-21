"""
Bonus B: Non-Deterministic TM Motoru (NondeterministicTM)
"""
from typing import List, Dict
from dataclasses import dataclass
from collections import deque

@dataclass
class NTMResult:
    accepted: bool
    accepting_paths: List[List[dict]]
    total_nodes_explored: int
    reason: str

class NondeterministicTM:
    def __init__(self, states: List[str], input_alphabet: List[str], tape_alphabet: List[str],
                 transitions: Dict, start_state: str, accept_states: List[str]):
        self.states = states
        self.input_alphabet = input_alphabet
        self.tape_alphabet = tape_alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
        self.blank_symbol = "B"
        
    def _clean_tape_string(self, tape: dict[int, str]) -> str:
        if not tape:
            return ""
        min_pos = min(tape.keys())
        max_pos = max(tape.keys())
        res = ""
        for i in range(min_pos, max_pos + 1):
            res += tape.get(i, self.blank_symbol)
        return res.strip(self.blank_symbol)
        
    def run(self, input_string: str, max_depth: int = 100, max_branches: int = 10000) -> NTMResult:
        init_tape = {i: char for i, char in enumerate(input_string)} if input_string else {0: self.blank_symbol}
        queue = deque([(self.start_state, init_tape, 0, [], 0)])
        
        nodes_explored = 0
        accepting_paths = []
        
        while queue:
            if nodes_explored >= max_branches:
                return NTMResult(len(accepting_paths) > 0, accepting_paths, nodes_explored, "max_branches_reached")
                
            current_state, tape, head_pos, path, depth = queue.popleft()
            nodes_explored += 1
            
            current_char = tape.get(head_pos, self.blank_symbol)
            
            new_path = path + [{
                "step": depth,
                "state": current_state,
                "tape": self._clean_tape_string(tape),
                "head": head_pos
            }]
            
            if current_state in self.accept_states:
                accepting_paths.append(new_path)
                continue
                
            if depth >= max_depth:
                continue
                
            choices = self.transitions.get((current_state, current_char), [])
            for next_state, write_char, move_dir in choices:
                new_tape = tape.copy()
                new_tape[head_pos] = write_char
                new_head_pos = head_pos + 1 if move_dir == "R" else head_pos - 1
                queue.append((next_state, new_tape, new_head_pos, new_path, depth + 1))
                
        reason = "completed" if len(accepting_paths) > 0 else "no_accepting_path"
        return NTMResult(len(accepting_paths) > 0, accepting_paths, nodes_explored, reason)
