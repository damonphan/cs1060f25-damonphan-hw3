HI_LO = {
    "A": -1, "2": +1, "3": +1, "4": +1, "5": +1, "6": +1,
    "7":  0, "8":  0, "9":  0,
    "10": -1, "J": -1, "Q": -1, "K": -1
}

def update_running_count(detected_ranks, current_count=0):
    for r in detected_ranks:
        current_count += HI_LO.get(r, 0)
    return current_count
