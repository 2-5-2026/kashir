def ran(s): #Funkcija za random koju mogu predvijeti za varanje :)
    return((1664525*s+1013904223) % (2**32))
    
def ai_choose(s): #AI
    rock=data["pl_r"]
    paper=data["pl_p"]
    scissors=data["pl_s"]
    l=[rock,paper,scissors]
    index=l.index(max(l))
    counter=index%3
    if max(l)/(sum(l)+1)>=0.8:
        s=ran(s)
        rng=s % 7
        if rng>=2:
            ai=counter
        else:
            ai=rng
    elif max(l)/(sum(l)+1)>=0.65:
        s=ran(s)
        rng=s % 6
        if rng>=2:
            ai=counter
        else:
            ai=rng
    elif max(l)/(sum(l)+1)>=0.5:
        s=ran(s)
        rng=s % 5
        if rng>=2:
            ai=counter
        else:
            ai=rng
    elif max(l)/(sum(l)+1)>=0.3:
        s=ran(s)
        rng=s % 4
        if rng>=2:
            ai=counter
        else:
            ai=rng
    else:
        s=ran(s)
        rng=s % 3
        ai=rng
    return(s,ai)
    
def load():
    try: #Proba otvoriti podatke
        with open("data.txt") as f:
            f=f.read()
            data=eval(f)
            if not(("pl_Wins" in data) and ("ai_Wins" in data) and ("draws" in data) and ("pl_r" in data) and ("pl_p" in data) and ("pl_s" in data) and ("seed" in data) and ("lang" in data)):
                data={"pl_Wins":0,"ai_Wins":0,"draws":0,"pl_r":0,"pl_p":0,"pl_s":0,"seed":0,"lang":0}
                print(f"Error: data.txt is wrongly formatted. \n-------------\n {f} \n-------------\nData reset has been done")
    except: #Ako ne generira novi session
        with open("data.txt", "w") as f:
            f.write('{"pl_Wins":0,"ai_Wins":0,"draws":0,"pl_r":0,"pl_p":0,"pl_s":0,"seed":0}')
            data={"pl_Wins":0,"ai_Wins":0,"draws":0,"pl_r":0,"pl_p":0,"pl_s":0,"seed":0}
    return(data)

#Početak
data={}
p=["Kamen","Papir", "Škare"]
ai=0

data=load()
lang_hr=["Kamen","Papir","Škare"]

#Inicijaliziraj ostale varijable
rock=data["pl_r"]
paper=data["pl_p"]
scissors=data["pl_s"]
seed=data["seed"]
l=[rock,paper,scissors]

print("Pobjede: "+ str(data["pl_Wins"]) + ", porazi: " + str(data["ai_Wins"]) + ", remiziranja: " + str(data["draws"]))

while True: #Glavni loop
    i=input("Upišite naredbu: ")
    if i=="stats":
        print("Pobjede: "+ str(data["pl_Wins"]) + ", porazi: " + str(data["ai_Wins"]) + ", remiziranja: " + str(data["draws"]))
    elif i=="kamen" or i=="Kamen" or i=="k" or i=="K":
        rock+=1
        seed,ai=ai_choose(seed)
        print("Kamen vs "+p[ai])
        if ai==0:
            data["draws"]+=1
        elif ai==1:
            data["ai_Wins"]+=1
        elif ai==2:
            data["pl_Wins"]+=1
    elif i=="papir" or i=="Papir" or i=="p" or i=="P":
        paper+=1
        seed,ai=ai_choose(seed)
        print("Papir vs "+p[ai])
        if ai==1:
            data["draws"]+=1
        elif ai==2:
            data["ai_Wins"]+=1
        elif ai==0:
            data["pl_Wins"]+=1
    elif i=="škare" or i=="Škare" or i=="š" or i=="Š" or i=="skare" or i=="Skare" or i=="s" or i=="S":
        scissors+=1
        seed,ai=ai_choose(seed)
        print("Škare vs "+p[ai])
        if ai==2:
            data["draws"]+=1
        elif ai==0:
            data["ai_Wins"]+=1
        elif ai==1:
            data["pl_Wins"]+=1
    elif i=="save" or i=="Save":
        data["seed"]=seed
        data["pl_r"]=rock
        data["pl_p"]=paper
        data["pl_s"]=scissors
        print(str(data))
        with open("data.txt", "w") as f:
            f.write(str(data))
        #load()
        
        
