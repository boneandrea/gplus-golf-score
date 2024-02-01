def prize(par, score):
    if score == 1:
        return "HOLEINONE"
    diff = score-par
    match diff:
        case -3:
            return "ALBATROSS"
        case -2:
            return "EAGLE"
        case -1:
            return "BIRDIE"
        case 0:
            return "PAR"
        case 1:
            return "BOGEY"
        case 2:
            return "DOUBLEBOGEY"
        case 3:
            return "TRIPLEBOGEY"
        case _:
            return ""
