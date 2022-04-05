# -*- coding: utf-8 -*-


class HPL:
    def __init__(self, msg):
        self.msg = msg
        self.msg_idx = 0
        self.memory = [0]
        self.memory_idx = 0
        self.values = []
        self.result = []
        self.refs = self._create_refs()

    def _create_refs(self):
        refs = {}
        init_idxs = []
        for idx, action in enumerate(self.msg):
            if action == "🤜":
                init_idxs.append(idx)
            elif action == "🤛":
                init_idx = init_idxs.pop()
                refs[idx] = init_idx
                refs[init_idx] = idx
        return refs

    def next_cell(self):
        if len(self.memory) - 1 <= self.memory_idx:
            self.memory.append(0)
        self.memory_idx += 1
        self.msg_idx += 1

    def prev_cell(self):
        if self.memory_idx == 0:
            self.memory = [0] + self.memory
        self.memory_idx = max(0, self.memory_idx - 1)
        self.msg_idx += 1

    def inc_cell(self):
        self.memory[self.memory_idx] = self.in_range(self.memory[self.memory_idx] + 1)
        self.msg_idx += 1

    def dec_cell(self):
        self.memory[self.memory_idx] = self.in_range(self.memory[self.memory_idx] - 1)
        self.msg_idx += 1

    def display(self):
        value = chr(self.memory[self.memory_idx])
        print(value, end="", flush=True)
        self.result.append(value)
        self.msg_idx += 1

    @staticmethod
    def in_range(number):
        return number % 256

    def jump_forward(self):
        if self.memory[self.memory_idx] == 0:
            self.msg_idx = self.refs[self.msg_idx]
        self.msg_idx += 1

    def jump_backward(self):
        if self.memory[self.memory_idx] != 0:
            self.msg_idx = self.refs[self.msg_idx]
        self.msg_idx += 1

    def translate(self):
        functions = {
            "👉": self.next_cell,
            "👈": self.prev_cell,
            "👆": self.inc_cell,
            "👇": self.dec_cell,
            "🤜": self.jump_forward,
            "🤛": self.jump_backward,
            "👊": self.display,
        }

        while self.msg_idx < len(self.msg):
            functions[self.msg[self.msg_idx]]()

        return "".join(self.result)


if __name__ == "__main__":
    with open("input.hand", "r") as src:
        msg = src.readline()

    result = HPL(msg.strip()).translate()

    print("".join(result))
