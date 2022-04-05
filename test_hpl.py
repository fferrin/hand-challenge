import pytest

from hpl import HPL


@pytest.mark.parametrize(
    ("msg", "expected"),
    (
            ("👉🤜👈👈👈👈👈👈👈👈👈👈👈🤛👊", {1: 13, 13: 1}),
            ("👉🤜👈👆🤜🤜🤜👇🤛👇🤛🤛👇🤛👊", {
                1: 13,
                4: 11,
                5: 10,
                6: 8,
                8: 6,
                10: 5,
                11: 4,
                13: 1,
            }),
    )
)
def test_stack(msg, expected):
    hpl = HPL(msg)
    refs = {}
    idxs = []
    for idx, action in enumerate(msg):
        if action == "🤜":
            idxs.append(idx)
        elif action == "🤛":
            init_idx = idxs.pop()
            refs[idx] = init_idx
            refs[init_idx] = idx

    assert hpl.refs == expected


@pytest.mark.parametrize(
    ("memory", "memory_idx", "expected_memory", "expected_memory_idx"),
    (
            ([0], 0, [0, 0], 1),
            ([0, 0], 0, [0, 0], 1),
            ([0, 0], 1, [0, 0, 0], 2),
    )
)
def test_next_cell(memory, memory_idx, expected_memory, expected_memory_idx):
    hpl = HPL("")

    hpl.memory = memory
    hpl.memory_idx = memory_idx

    hpl.next_cell()

    assert hpl.memory == expected_memory
    assert hpl.memory_idx == expected_memory_idx


@pytest.mark.parametrize(
    ("memory", "memory_idx", "expected_memory", "expected_memory_idx"),
    (
            ([0, 0], 1, [0, 0], 0),
            ([0, 0], 0, [0, 0, 0], 0),
            ([0, 0, 0], 2, [0, 0, 0], 1),
    )
)
def test_prev_cell(memory, memory_idx, expected_memory, expected_memory_idx):
    hpl = HPL("")

    hpl.memory = memory
    hpl.memory_idx = memory_idx

    hpl.prev_cell()

    assert hpl.memory == expected_memory
    assert hpl.memory_idx == expected_memory_idx


@pytest.mark.parametrize(
    ("memory", "memory_idx", "expected_memory", "expected_memory_idx"),
    (
            ([0, 1, 2], 1, [0, 2, 2], 1),
            ([0, 255, 2], 1, [0, 0, 2], 1),
    )
)
def test_inc_cell(memory, memory_idx, expected_memory, expected_memory_idx):
    hpl = HPL("")

    hpl.memory = memory
    hpl.memory_idx = memory_idx

    hpl.inc_cell()

    assert hpl.memory == expected_memory
    assert hpl.memory_idx == expected_memory_idx


@pytest.mark.parametrize(
    ("memory", "memory_idx", "expected_memory", "expected_memory_idx"),
    (
            ([0, 1, 2], 1, [0, 0, 2], 1),
            ([0, 0, 2], 1, [0, 255, 2], 1),
    )
)
def test_dec_cell(memory, memory_idx, expected_memory, expected_memory_idx):
    hpl = HPL("")

    hpl.memory = memory
    hpl.memory_idx = memory_idx

    hpl.dec_cell()

    assert hpl.memory == expected_memory
    assert hpl.memory_idx == expected_memory_idx


@pytest.mark.parametrize(
    ("msg", "memory", "memory_idx", "msg_idx", "expected_msg_idx"),
    (
            # 0 1  2 3 4 5 6  7 8 9
            ("👉🤜👈👆🤜👇🤛👇🤛👊", [1, 0, 1, 2], 1, 1, 9),
            ("👉🤜👈👆🤜👇🤛👇🤛👊", [1, 0, 1, 2], 1, 4, 7),
            ("👉🤜👈👆🤜👇🤛👇🤛👊", [1, 1, 1, 2], 1, 1, 2),
            ("👉🤜👈👆🤜👇🤛👇🤛👊", [1, 1, 1, 2], 1, 4, 5),
            # 0  1 2 3 4 5 6  7 8 9 10 1 2 3 4
            ("👉🤜👈👆🤜🤜🤜👇🤛👇🤛🤛👇🤛👊", [1, 0, 1, 2], 1, 6, 9),
            ("👉🤜👈👆🤜🤜🤜👇🤛👇🤛🤛👇🤛👊", [1, 0, 1, 2], 1, 6, 9),
    )
)
def test_jump_forward(msg, memory, memory_idx, msg_idx, expected_msg_idx):
    hpl = HPL(msg)
    hpl.memory = memory
    hpl.memory_idx = memory_idx
    hpl.msg_idx = msg_idx

    hpl.jump_forward()

    assert hpl.msg_idx == expected_msg_idx


@pytest.mark.parametrize(
    ("msg", "memory", "memory_idx", "msg_idx", "expected_msg_idx"),
    (
            # 0 1  2 3 4 5 6  7 8 9
            # In loop
            ("👉🤜👈👆🤜👇🤛👇🤛👊", [1, 1, 1, 2], 1, 6, 5),
            ("👉🤜👈👆🤜👇🤛👇🤛👊", [1, 1, 1, 2], 1, 8, 2),
            # Not in loop
            ("👉🤜👈👆🤜👇🤛👇🤛👊", [1, 0, 1, 2], 1, 6, 7),
            ("👉🤜👈👆🤜👇🤛👇🤛👊", [1, 0, 1, 2], 1, 8, 9),
            # 0  1 2 3 4 5  6 7 8 9 10 1 2 3 4
            # In loop
            ("👉🤜👈👆🤜🤜🤜👇🤛👇🤛🤛👇🤛👊", [1, 1, 1, 2], 1, 8, 7),
            ("👉🤜👈👆🤜🤜🤜👇🤛👇🤛🤛👇🤛👊", [1, 1, 1, 2], 1, 10, 6),
            ("👉🤜👈👆🤜🤜🤜👇🤛👇🤛🤛👇🤛👊", [1, 1, 1, 2], 1, 11, 5),
            ("👉🤜👈👆🤜🤜🤜👇🤛👇🤛🤛👇🤛👊", [1, 1, 1, 2], 1, 13, 2),
            # Not in loop
            ("👉🤜👈👆🤜🤜🤜👇🤛👇🤛🤛👇🤛👊", [1, 0, 1, 2], 1, 8, 9),
            ("👉🤜👈👆🤜🤜🤜👇🤛👇🤛🤛👇🤛👊", [1, 0, 1, 2], 1, 10, 11),
            ("👉🤜👈👆🤜🤜🤜👇🤛👇🤛🤛👇🤛👊", [1, 0, 1, 2], 1, 11, 12),
            ("👉🤜👈👆🤜🤜🤜👇🤛👇🤛🤛👇🤛👊", [1, 0, 1, 2], 1, 13, 14),
    )
)
def test_jump_backward(msg, memory, memory_idx, msg_idx, expected_msg_idx):
    hpl = HPL(msg)
    hpl.memory = memory
    hpl.memory_idx = memory_idx
    hpl.msg_idx = msg_idx

    hpl.jump_backward()

    assert hpl.msg_idx == expected_msg_idx


@pytest.mark.parametrize(
    ("memory", "memory_idx", "letter"),
    (
            ([0, 1, 2, 97, 4, 5], 3, "a"),
            ([0, 1, 100, 3, 4, 5], 2, "d"),
    )
)
def test_display(memory, memory_idx, letter):
    hpl = HPL("")
    hpl.memory = memory
    hpl.memory_idx = memory_idx
    hpl.display()
    assert hpl.result == [letter]


def test_in_range():
    assert 123 == HPL.in_range(123)
    assert 0 == HPL.in_range(0)
    assert 255 == HPL.in_range(255)
    assert 0 == HPL.in_range(255 + 1)
    assert 255 == HPL.in_range(0 - 1)


def test_challenge():
    msg = "👇🤜👇👇👇👇👇👇👇👉👆👈🤛👉👇👊👇🤜👇👉👆👆👆👆👆👈🤛👉👆👆👊👆👆👆👆👆👆👆👊👊👆👆👆👊"
    assert HPL(msg).translate() == "Hello"

    msg = "👇🤜👇👇👇👇👇👇👇👉👆👈🤛👉👇👊👇🤜👇👉👆👆👆👆👆👈🤛👉👆👆👊👆👆👆👆👆👆👆👊👊👆👆👆👊👊👊👊"
    assert HPL(msg).translate() == "Helloooo"
