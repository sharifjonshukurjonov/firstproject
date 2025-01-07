def pawn_check(x1, y1, x2, y2):
    if y1 == 2:
        return x1 == x2 and y2 - y1 == 1 or y2 - y1 == 2
    return x1 == x2 and y2 - y1 == 1

# print(pawn_check(2, 3, 2, 4))

def rook_check(x1, y1, x2, y2):
    return x1 == x2 or y1 == y2