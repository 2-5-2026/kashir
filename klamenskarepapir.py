def ran(s): #Funkcija za random koju mogu predvijeti za varanje :)
    return((1664525*s+1013904223) % (2**32))
    
def ai_choose(s): #AI
    rock=data["pl_r"]
    paper=data["pl_p"]
    scissors=data["pl_s"]
    l=[rock,paper,scissors]
    index=l.index(max(l))
    counter=(index+1)%3
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
                data={"pl_Wins":0,"ai_Wins":0,"draws":0,"pl_r":0,"pl_p":0,"pl_s":0,"seed":0,"lang":0,"lang":"en"}
                print(lang[7][0]+f+lang[7][1])
    except: #Ako ne generira novi session
        with open("data.txt", "w") as f:
            f.write('{"pl_Wins":0,"ai_Wins":0,"draws":0,"pl_r":0,"pl_p":0,"pl_s":0,"seed":0,"lang":"en"}')
            data={"pl_Wins":0,"ai_Wins":0,"draws":0,"pl_r":0,"pl_p":0,"pl_s":0,"seed":0,"lang":"en"}
    return(data)

def load_lang(l):
    with open("lang_"+l+".txt",encoding="utf-8") as f:
        f=f.read()
        return(f)

#Početak
data={}
ai=0
lang=eval(load_lang("en"))
data=load()
lang=eval(load_lang(data["lang"]))
p=[lang[0],lang[2],lang[1]]


#Inicijaliziraj ostale varijable
rock=data["pl_r"]
paper=data["pl_p"]
scissors=data["pl_s"]
seed=data["seed"]
l=[rock,paper,scissors]

print(lang[9]+ str(data["pl_Wins"]) + lang[10] + str(data["ai_Wins"]) + lang[11] + str(data["draws"]))

while True: #Glavni loop
    i=input(lang[12])
    if i==lang[8]:
        print(lang[9]+ str(data["pl_Wins"]) + lang[10] + str(data["ai_Wins"]) + lang[11] + str(data["draws"]))
    elif i in lang[3]:
        rock+=1
        seed,ai=ai_choose(seed)
        print(lang[0]+" vs "+p[ai])
        if ai==0:
            data["draws"]+=1
            print(lang[17])
        elif ai==1:
            data["ai_Wins"]+=1
            print(lang[16])
        elif ai==2:
            data["pl_Wins"]+=1
            print(lang[15])
    elif i in lang[4]:
        paper+=1
        seed,ai=ai_choose(seed)
        print(lang[2]+" vs "+p[ai])
        if ai==1:
            data["draws"]+=1
            print(lang[17])
        elif ai==2:
            data["ai_Wins"]+=1
            print(lang[16])
        elif ai==0:
            data["pl_Wins"]+=1
            print(lang[15])
    elif i in lang[5]:
        scissors+=1
        seed,ai=ai_choose(seed)
        print(lang[1]+" vs "+p[ai])
        if ai==2:
            data["draws"]+=1
            print(lang[17])
        elif ai==0:
            data["ai_Wins"]+=1
            print(lang[16])
        elif ai==1:
            data["pl_Wins"]+=1
            print(lang[15])
    elif i in lang[6]:
        data["seed"]=seed
        data["pl_r"]=rock
        data["pl_p"]=paper
        data["pl_s"]=scissors
        #print(str(data))
        with open("data.txt", "w") as f:
            f.write(str(data))
        #load()
    elif i=="language":
        data["lang"]=input(lang[13])
        lang=eval(load_lang(data["lang"]))
        p=[lang[0],lang[2],lang[1]]
    elif i==lang[18]:
        break
    else:
        print(lang[14])
        
        
