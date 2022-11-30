from basis import getBasis
from predicate import operator,predicate
from computation import computation,process,event,eventStatus

def printBasis(basis):
    idx=0
    print("total semiregular structure number: ",len(basis))
    for s in basis:
        print("semiregular structure ",idx)
        idx+=1
        print("slice:")
        if s[0]=={}:
            print("empty")
        else:
            printGraph(s[0])
        print("stable structure")
        if s[1]==[]:
            print("empty")
        else:
            for maxCut in s[1]:
                print(maxCut)
def printGraph(g):
    for k,v in g.items():
        print("(",k[0],",",k[1],")",end=" :")
        for n in v:
            print("(",n[0],",",n[1],")",end=" ")
        print()
events1=[]
tempEvent=event(0,0,eventStatus.INTERNAL)
events1.append(tempEvent)
tempEvent=event(1,2,eventStatus.RECEIVE,(1,1),(0,1))
events1.append(tempEvent)
tempEvent=event(2,4,eventStatus.INTERNAL)
events1.append(tempEvent)
tempEvent=event(3,5,eventStatus.INTERNAL)
events1.append(tempEvent)
p1=process(0,events1)

events2=[]
tempEvent=event(0,0,eventStatus.INTERNAL)
events2.append(tempEvent)
tempEvent=event(1,0,eventStatus.SEND,(1,1),(0,1))
events2.append(tempEvent)
tempEvent=event(2,2,eventStatus.INTERNAL)
events2.append(tempEvent)
tempEvent=event(3,6,eventStatus.INTERNAL)
events2.append(tempEvent)
p2=process(1,events2)

processes=[p1,p2]
comp=computation(processes)

def localPredicate1(state,computation):
    p=computation.processes[0]
    e=p.events[state[0]]
    v=e.value
    if v>=2 and v<=4:
        return True
    else:
        return False

def localPredicate2(state,computation):
    p=computation.processes[1]
    e=p.events[state[1]]
    v=e.value
    if v!=2:
        return True
    else:
        return False

p1=predicate(True,localPredicate1)
p2=predicate(True,localPredicate2)
pred1=predicate(False,p1,p2,operator.CONJUNCTION)
pred2=predicate(False,pred1,None,operator.EF)
basis=getBasis(comp,pred2)
#print basis
printBasis(basis)