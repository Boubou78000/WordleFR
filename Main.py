import progressbar
import os

Words5=[]
Words6=[]
Words4=[]

Path=os.path.dirname(os.path.abspath(__file__))+"\\Words"

with open(Path+"5_.txt",'r') as f:
    Words5.append(f.read().split('\n'))

with open(Path+"5.txt",'r') as f:
    Words5.append(f.read().split('\n'))

with open(Path+"6_.txt",'r') as f:
    Words6.append(f.read().split('\n'))

with open(Path+"6.txt",'r') as f:
    Words6.append(f.read().split('\n'))

with open(Path+"4_.txt",'r') as f:
    Words4.append(f.read().split('\n'))

with open(Path+"4.txt",'r') as f:
    Words4.append(f.read().split('\n'))

def CreateBar():
    global bar
    bar = progressbar.ProgressBar(maxval=100, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()

def GenerateSet():
    global WordsWithout
    global WordsWithoutPlace
    global WordsWithPlace
    for i in Words[0]:
        for j in range(26):
            if ABC[j] in i:
                #WordsWith[j].add(i)
                for k in range(len(i)):
                    if i[k]==ABC[j]:
                        WordsWithPlace[j][k].add(i)
                    else:
                        WordsWithoutPlace[j][k].add(i)
            else:
                WordsWithout[0][j].add(i)


def GetPossibles(Data, poss):
    global WordsData
    Possibilities=poss.copy()
    for i in Data:
        Possibilities.intersection_update(WordsData[i[0]][i[1]][i[2]])
    return Possibilities

def Check(Word, Good, Yellow, Wrong):
    for i in Wrong:
        if i in Word:
            return False
    for i in range(len(Good)):
        if Good[i]==' ':
            continue
        if not Good[i]==Word[i]:
            return False
    for i in Yellow:
        if not i in Word:
            return False
    return True

def GetStats(Word, Word2): #deprecated
    g=""
    w=""
    d=[]
    for i in range(len(Word)):
        if Word[i] in Word2:
            g+=Word[i]
            if Word[i]==Word2[i]:
                d+=[False]
            else:
                d+=[True]
        else:
            w+=Word[i]
            d+=[None]
    return g, w, d

def NewStats(Word, Word2, k=False):
    global AlreadyKnown

    Data=[]
    good=set()
    bad=set()
    for i in range(len(Word)):
        if Word[i] in Word2:
            if Word[i]==Word2[i]:
                Data.append((1,ABC.index(Word[i]),i))
                good.add(Word[i])
            else:
                Data.append((2,ABC.index(Word[i]),i))
                good.add(Word[i])
        else:
            bad.add(Word[i])

    bad.difference_update(good)

    for i in list(bad):
        Data.append((0,0,ABC.index(i)))

    set_data=set()
    for i in Data:
        set_data.add(i)
    set_data.difference_update(AlreadyKnown[Word2])

    if k:
        AlreadyKnown.update({Word2: AlreadyKnown[Word2].union(set_data)})

    return Data

def GlobalFitness(Word, Data):
    Fit=0
    for i in Data:
        Fit+=NewFitness(Word, i)
    return Fit/len(Words[0])

def Fitness(Word, Word2): #deprecated
    Fit=0
    for i in range(len(Word2)):
        if Word2[i]==Word[i] and not True in [Word2[i]==Known[k][i] for k in range(len(Known))]:
            Fit+=2/10
        elif Word2[i] in Word and not True in [Word2[i] in Known[k] for k in range(len(Known))]:
            Fit+=1/10
        
    return Fit

def NewFitness(Word, Word2):
    if Word==Word2:
        return 0
    Poss=Known[Word2]
    Data=NewStats(Word, Word2)
    Poss=GetPossibles(Data, Poss)
    #GlobalPossibles[Word].update({Word2:Poss})
    return len(Poss)

#["taire","clous","demon","prevu"]

def Statistics(n, previous=[]):

    InitKnown()

    for i in previous:
        UpdateKnown(i)

    for _ in range(n):

        Word=input("Play which word? ")

        print(GlobalFitness(Word, Words[0]))

        UpdateKnown(Word)

def UpdateKnown(Word):
    for i in Words[0]:
        Known.update({i:GetPossibles(NewStats(Word, i, True),Known[i])})

def FindWord(n, previous=[]):
    global Known
        
    InitKnown()

    for i in previous:
        UpdateKnown(i)

    for _ in range(n):

        CreateBar()

        Best=""
        BestFit=1000000000

        for i in range(len(Words[1])):
            #print(" "+Words[0][i])
            Current=GlobalFitness(Words[1][i], Words[0])
            bar.update(100*(i/len(Words[1])))
            if Current<BestFit:
                BestFit=Current
                Best=Words[1][i]

        bar.finish()

        print(Best)
        print(BestFit)

        UpdateKnown(Best)

def Play(previous=[]):

    InitKnown()

    for i in previous:
        UpdateKnown(i)

    Possible=set(Words[0])
    for t in range(6):

        CreateBar()

        if t==0:
            Best=DataBase[len(Words[0][0])][0]

        elif len(Possible)==1:
            Best=list(Possible)[0]

        else:
            Best_=False
            Best=""
            BestFit=1000000000

            for i in range(len(Words[1])):
                Current=GlobalFitness(Words[1][i], Possible)
                bar.update(i/len(Words[1])*100)
                #print(f"{Words[0][i]} {Current} {(100*(i/len(Words[0])))}%")
                #print(i, Current*100)
                if Current<BestFit or (Current==BestFit and Words[1][i] in Possible and not Best_) or (Words[1][i] in Words[0] and i in Possible):
                    #print(BestFit, Best, Current, list(Possible)[i], str(100*(i/len(Possible)))+"%")
                    if Words[1][i] in Words[0]:
                        Best_=True
                    if Current<BestFit and not Words[1][i] in Words[0]:
                        Best_=False
                    if HardMode:
                        if not Words[1][i] in Possible:
                            continue
                    BestFit=Current
                    Best=Words[1][i]

        bar.finish()

        print(f"""Word: {Best}""")

        UpdateKnown(Best)

        _input=input()

        if _input=="win":
            print("The AI beat the wordle!")
            break
            
        Data=[]
        good=set()
        bad=set()

        for i in range(len(_input)):
            if _input[i]=="D":
                #print(Possible)
                #print(g, y, b)
                pass
            elif _input[i]=="*":
                Data.append((2,ABC.index(Best[i]),i))
                good.add(Best[i])
            elif _input[i]=="_":
                Data.append((1,ABC.index(Best[i]),i))
                good.add(Best[i])
            else:
                bad.add(Best[i])

        bad.difference_update(good)
        
        for i in bad:
            Data.append((0,0,ABC.index(i)))

        Possible=GetPossibles(Data, Possible)

        print(Possible)

        """for i,i2,i3 in Data:
            print(["Gray","Green","Yellow"][i])
            if i==0:
                print(ABC[i3])
            else:
                print(ABC[i2])
                print(i3)"""

        Possible.difference_update({Best})

        if len(Possible)==0:
            print("The AI is broken, sorry :\\")
            break
    
    else:
        print("The wordle beat the AI!")

Console=True

AllWords=[Words4, Words5, Words6]
if Console:
    Words=eval("Words"+input("How many letters? "))
    HardMode=eval(input("Hard mode? "))

def InitKnown():
    global Known
    global AlreadyKnown

    AlreadyKnown={}
    Known={}

    for i in Words[0]:
        Known.update({i:set(Words[0])})
        AlreadyKnown.update({i:set()})

InitKnown()

ABC="azertyuiopqsdfghjklmwxcvbn"

#WordsWith=[set() for _ in range(26)]
WordsWithout=[[set() for _ in range(26)]]
WordsWithPlace=[[set() for _ in range(len(Words[0][0]))] for _ in range(26)]
WordsWithoutPlace=[[set() for _ in range(len(Words[0][0]))] for _ in range(26)]

"""GlobalPossibles={}

k={}
for j in Words[0]:
    k.update({j:set(Words[0])}) #for each good word, the already computed poss

for i in range(len(Words[0])):
    GlobalPossibles.update({Words[0][i]: k})"""

GenerateSet()

WordsData=[WordsWithout, WordsWithPlace, WordsWithoutPlace]

print("Sets generated!")

DataBase={4: ("raie","stuc","pond","film","bava"), 5: ("tarie","clous","benef","vampa","grand"), 6: ("tarins","copule","dogmes","evasif","bicher")}

if Console:
    Play()
