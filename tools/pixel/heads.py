"""손으로 찍은 머리(얼굴+머리카락) 도트. 오른쪽을 보는 3/4 측면."""
COL = {
    'O': '#2a1a1f',
    'h': '#c98a52', 'H': '#97582d', 'd': '#6b3819', 'D': '#47210c',     # 머리카락
    's': '#ffe6c8', 'S': '#f7c29a', 'k': '#dc9670', 'K': '#b8714f',     # 피부
    'e': '#2a1a1f', 'w': '#ffffff', 'i': '#6a4430',                      # 눈
    'b': '#f69c88', 'm': '#a8503a',                                      # 볼, 입
}
HEAD13 = [
    "......OOOOO.......",
    "....OOhhhhHOO..O..",
    "...OhhhHHHHHHOOHO.",
    "..OhHHHHHHHHHHHHdO",
    ".OHhHHHHHHHHHHHHdO",
    "OdHHHHHHdHHHHHdHdO",
    "OdHHHdHdSdHHdSSdO.",
    "OdHHdKSSSSdSSSSSO.",
    "OdHdKkSSSewSSewSO.",
    ".OddKkSSSeiSSeiSO.",
    ".OdOkSSbSSSSSSSbO.",
    "..O.OkSSSSSSmSSO..",
    ".....OkkSSSSSSO...",
    "......OOOOOOOO....",
]
HEAD11 = [
    ".....OOOO.......",
    "...OOhhhHOO..O..",
    "..OhhHHHHHHOOHO.",
    ".OhHHHHHHHHHHHdO",
    "OdHHHHHHdHHHdHdO",
    "OdHHdHdSdHdSSdO.",
    "OdHdKSSSSSSSSSO.",
    "OddKkSSewSSSewO.",
    ".OdOkSbSSSSSSbO.",
    "..O.OkSSSSmSSO..",
    ".....OkkSSSSO...",
    "......OOOOOO....",
]
HEAD16 = [
    ".......OOOOOO........",
    ".....OOhhhhhHOO...O..",
    "....OhhhHHHHHHHOO.OHO",
    "...OhhHHHHHHHHHHHOHHO",
    "..OhHHHHHHHHHHHHHHHdO",
    ".OHhHHHHHHHHHHHHHHHdO",
    "OdHHHHHHHdHHHHHHdHHdO",
    "OdHHHHdHHdHHHdHHdHdO.",
    "OdHHHdHdSSdHHdSSSSdO.",
    "OdHHdKSSSSSdSSSSSSSO.",
    "OdHdKkSSSSSSSSSSSSSO.",
    "OdHdKkSSSSewSSSSewSO.",
    ".OddKkSSSSeeSSSSeeSO.",
    ".OdOkSSSSSeiSSSSeiSO.",
    "..O.OkSbbSSSSSSSSSbO.",
    "....OkSSSSSSSSmmSSO..",
    ".....OkkSSSSSSSSSO...",
    "......OOkkkkkkkOO....",
    "........OOOOOOO......",
]
def head_pixels(rows):
    out = {}
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != '.': out[(x, y)] = COL[ch]
    return out, len(rows[0]), len(rows)
