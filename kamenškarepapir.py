import random

#kamen škare papir
#a = {"kamen" : 1, "škare" : 2, "papir" : 3}
a = ["kamen", "škare", "papir"]

ime = input("Unesi ime igrača: ")

win = ("igrač pobjeđuje")
loss = ("igrač gubi")

while True:
    igr= input("Kamen škare papir... ")
    print(ime, ": ", igr)

    b =random.choice(a)
    print("Kompjuter: ", b)

    if igr == "kamen" and b == "škare":
        print(win)
    elif igr == "kamen" and b == "papir":
        print(loss)
    elif igr == "škare" and b == "kamen":
        print(loss)
    elif igr == "škare" and b == "papir":
        print(win)
    elif igr == "papir" and b == "škare":
        print(loss)
    elif igr == "papir" and b == "kamen":
        print(win)
    else:
        print("remi")

win_num = 0

def moja_funkcija():
    global win_num
    win_num += 1
    print("Pozvana!")

moja_funkcija()
moja_funkcija()
moja_funkcija()

print("Pozvana je", win_num, "puta")
