"""
Bölüm 1: Tek şeritli TM Motoru (SingleTapeTM)

Deterministic single-tape Turing makinelerini çalıştıran temel Python kütüphanesi.
"""
import yaml
from dataclasses import dataclass, field


@dataclass
class Configuration:
    """Bir hesaplama adımının anlık görüntüsü (snapshot).

    Attributes:
        step: Adım numarası (0'dan başlar).
        state: O adımdaki durum etiketi.
        tape: Şeridin tamamını temsil eden string (kafa konumu köşeli parantezli).
        head_position: Kafanın o anki tam sayı konumu.
    """
    step: int
    state: str
    tape: str
    head_position: int


@dataclass
class RunResult:
    """TM çalıştırma sonucu.

    Attributes:
        accepted: Makine kabul durumuna ulaştıysa True.
        reason: 'accept' | 'reject' | 'no_transition' | 'timeout'
        final_tape: Durduğundaki şerit içeriği (baştaki/sondaki blank'lar temizlenmiş).
        steps: Toplam kaç adım atıldı.
        history: Her adım için Configuration nesnelerinin listesi.
    """
    accepted: bool
    reason: str
    final_tape: str
    steps: int
    history: list[Configuration]


class SingleTapeTM:
    """Deterministic tek-şeritli Turing makinesi motoru.

    Şerit dahili olarak dict[int, str] (sparse) olarak tutulur;
    bu sayede hem sol hem sağ sonsuz genişleyebilir.

    Example:
        tm = SingleTapeTM.from_yaml("machines/binary_increment.yaml")
        result = tm.run("1011", max_steps=1000, verbose=False)
        assert result.accepted is True
    """

    def __init__(
        self,
        states: list[str],
        input_alphabet: list[str],
        tape_alphabet: list[str],
        transitions: dict,
        start_state: str,
        accept_states: list[str],
        reject_states: list[str] = None,
        blank: str = "B",
    ):
        """TM'i doğrudan parametrelerle başlat.

        Args:
            states: Durum listesi.
            input_alphabet: Giriş alfabesi.
            tape_alphabet: Şerit alfabesi (blank dahil).
            transitions: {(durum, okunan): (sonraki_durum, yazılan, yön)} sözlüğü.
            start_state: Başlangıç durumu.
            accept_states: Kabul durumları listesi.
            reject_states: Red durumları listesi (opsiyonel).
            blank: Blank sembol (varsayılan 'B').
        """
        self.states = states
        self.input_alphabet = input_alphabet
        self.tape_alphabet = tape_alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
        self.reject_states = reject_states or []
        self.blank_symbol = blank

    @classmethod
    def from_yaml(cls, file_path: str) -> "SingleTapeTM":
        """YAML dosyasından TM yükle.

        Args:
            file_path: YAML dosyasının yolu.

        Returns:
            SingleTapeTM örneği.

        Raises:
            ValueError: YAML okunamazsa veya zorunlu alan eksikse.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"YAML okuma hatası: {e}")
        except OSError as e:
            raise ValueError(f"YAML okuma hatası: {e}")

        required_keys = [
            "states", "input_alphabet", "tape_alphabet",
            "transitions", "start_state", "accept_states",
        ]
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Eksik anahtar: {key}")

        blank = str(data.get("blank", "B"))

        trans_dict = {}
        for tr in data["transitions"]:
            if not all(k in tr for k in ["state", "read", "next", "write", "move"]):
                raise ValueError(f"Geçiş kuralında eksik anahtar var: {tr}")
            trans_dict[(tr["state"], str(tr["read"]))] = (
                tr["next"], str(tr["write"]), tr["move"]
            )

        return cls(
            states=data["states"],
            input_alphabet=[str(x) for x in data["input_alphabet"]],
            tape_alphabet=[str(x) for x in data["tape_alphabet"]],
            transitions=trans_dict,
            start_state=data["start_state"],
            accept_states=data["accept_states"],
            reject_states=data.get("reject_states", []),
            blank=blank,
        )

    def _tape_to_string(self, tape: dict[int, str], head_pos: int) -> str:
        """Şeridi kafa konumu köşeli parantez içinde string olarak döndür.

        Args:
            tape: Sparse şerit sözlüğü.
            head_pos: Kafanın konumu.

        Returns:
            Okunabilir şerit string'i. Örn: '10[1]1B'
        """
        if not tape:
            return f"[{self.blank_symbol}]"
        min_pos = min(min(tape.keys()), head_pos)
        max_pos = max(max(tape.keys()), head_pos)

        res = ""
        for i in range(min_pos, max_pos + 1):
            char = tape.get(i, self.blank_symbol)
            if i == head_pos:
                res += f"[{char}]"
            else:
                res += char
        return res

    def _clean_tape_string(self, tape: dict[int, str]) -> str:
        """Şeridi baştaki ve sondaki blank'lar temizlenmiş string olarak döndür.

        Args:
            tape: Sparse şerit sözlüğü.

        Returns:
            Temizlenmiş şerit string'i.
        """
        if not tape:
            return ""
        min_pos = min(tape.keys())
        max_pos = max(tape.keys())
        res = ""
        for i in range(min_pos, max_pos + 1):
            res += tape.get(i, self.blank_symbol)
        return res.strip(self.blank_symbol)

    def run(
        self,
        input_string: str,
        max_steps: int = 1000,
        verbose: bool = False,
    ) -> RunResult:
        """TM'i verilen girdi üzerinde çalıştır.

        Args:
            input_string: Şeride yazılacak girdi.
            max_steps: İzin verilen maksimum adım sayısı.
            verbose: True ise her adımı stdout'a yazar.

        Returns:
            RunResult: Kabul/ret durumu, şerit, adım sayısı ve tarihçe.
        """
        tape: dict[int, str] = {i: ch for i, ch in enumerate(input_string)}
        if not tape:
            tape[0] = self.blank_symbol

        head_pos = 0
        current_state = self.start_state
        steps = 0
        history: list[Configuration] = []

        while steps < max_steps:
            current_char = tape.get(head_pos, self.blank_symbol)
            tape_str = self._tape_to_string(tape, head_pos)

            trans = self.transitions.get((current_state, current_char))
            move_dir = trans[2] if trans else "-"

            history.append(Configuration(
                step=steps,
                state=current_state,
                tape=tape_str,
                head_position=head_pos,
            ))

            if verbose:
                print(
                    f"Adım {steps} | Durum: {current_state} | "
                    f"Şerit: {tape_str} | Hareket: {move_dir}"
                )

            if current_state in self.accept_states:
                return RunResult(True, "accept", self._clean_tape_string(tape), steps, history)

            if current_state in self.reject_states:
                return RunResult(False, "reject", self._clean_tape_string(tape), steps, history)

            if not trans:
                return RunResult(False, "no_transition", self._clean_tape_string(tape), steps, history)

            next_state, write_char, move_dir = trans
            tape[head_pos] = write_char
            current_state = next_state

            if move_dir == "R":
                head_pos += 1
            elif move_dir == "L":
                if head_pos == 0:
                    # Kafa sola taşmaya çalışıyor: pozisyonu negatife izin ver
                    # (sparse dict'te sorun yok), ancak head_position < 0 olduğunda
                    # bir sonraki adımda tape[-1] Python listesi gibi davranmaz.
                    head_pos -= 1
                else:
                    head_pos -= 1

            steps += 1

        # Son adımı da history'ye ekle
        history.append(Configuration(
            step=steps,
            state=current_state,
            tape=self._tape_to_string(tape, head_pos),
            head_position=head_pos,
        ))
        return RunResult(False, "timeout", self._clean_tape_string(tape), steps, history)
