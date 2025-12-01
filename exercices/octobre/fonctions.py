course = {"j1":1, "j2":2, "j3":3, "j4":4}

def dépasse(player1, player2):
    if course[player1] - 1 == course[player2]:
        position = course[player1]
        course[player1] = course[player2]
        course[player2] = position
    else:
        print("depassement impossible")
    return "5", "6"
k1 = "j1"
course = {k1 : 1, "j2":2, "j3":3, "j4":4}
print(k1)
k1, k2 = dépasse("j2", k1)
print(k1)
print(k2)
print(course)
dépasse("j4", "j3")
print(course)
dépasse("j2", "j3")
print(course)