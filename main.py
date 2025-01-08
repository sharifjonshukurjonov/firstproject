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
    return (x1 - x2) ** 2 + (y1 -y2) ** 2 == 5

# print(rook_check(1, 1, 8, 2))


def queen_check(x1, y1, x2, y2):
    return abs(x1 - x2) == abs(y1 - y2) or x1 == x2 or y1 == y2

# print(rook_check(1, 1, 8, 2))

def king_check(x1, y1, x2, y2):
    ox = abs(x1 - x2)
    oy = abs(y1 - y2)
    return ox + oy <= 2

print(king_check(2,1,2,8))