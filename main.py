def pawn_check(x1, y1, x2, y2):
    if y1 == 2:
        return x1 == x2 and y2 - y1 == 1 or y2 - y1 == 2
    return x1 == x2 and y2 - y1 == 1

# print(pawn_check(2, 3, 2, 4))

def rook_check(x1, y1, x2, y2):
    return x1 == x2 or y1 == y2

# print(rook_check(1, 1, 8, 2))


def bishop_check(x1, y1, x2, y2):
    return abs(x1 - x2) == abs(y1 - y2)

# print(rook_check(1, 1, 8, 2))



def knight_check(x1, y1, x2, y2):
    ox = abs(x1 - x2)
    oy = abs(y1 - y2)
    return ox == 2 and oy == 1 or ox == 1 and oy == 2