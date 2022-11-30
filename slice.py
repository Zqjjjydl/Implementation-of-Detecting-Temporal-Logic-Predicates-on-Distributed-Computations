from computation import eventStatus,computation,event,process
import copy
def getSlice(computation,predicate):
    #build consistent cut lattice
    consistentStateSet=getConsistentStates(computation)
    #get sub lattice
    subLattice=[]
    for s in consistentStateSet:
        if predicate(s,computation):
            subLattice.append(s)
    #get join−irreducible ones
    joinIrreducibleSet=[]
    inDegree=dict()
    g=buildGraph(subLattice)
    for v,neighbour in g.items():
        if v not in inDegree:
            inDegree[tuple(v)]=0
        for u in neighbour:
            if tuple(u) in inDegree:
                inDegree[tuple(u)]=inDegree[tuple(u)]+1
            else:
                inDegree[tuple(u)]=1
    for v,d in inDegree.items():
        if d==1:
            joinIrreducibleSet.append(v)
    g=buildGraph(joinIrreducibleSet)
    return g

def isConsistent(state,senderInfo):
    for i,eventId in enumerate(state):
        #for each process check whether the sender has been received
        sender=senderInfo[i][eventId]
        for s in sender:
            if s[1]>state[s[0]]:
                return False
    return True

def buildGraph(vertex):#return graph given some ordered vertex
    g=dict()
    for idx,v in enumerate(vertex):
        largerV=[]
        for u in vertex:
            if u==v:
                continue
            isLarger=True
            for i in range(len(u)):
                if u[i]<v[i]:
                    isLarger=False
            if isLarger:
                largerV.append(u)
        sup=[]
        for u in largerV:
            isLarger=False#true if u is larger than any w
            for w in largerV:
                if w==u:
                    continue
                isLargerW=True#true if u is larger than w
                for i in range(len(u)):
                    if w[i]>u[i]:
                        isLargerW=False
                if isLargerW:
                    isLarger=True
                    break
            if not isLarger:
                sup.append(u)
        g[tuple(v)]=sup
    return g

def getConsistentStates(computation):
    processSize=len(computation.processes)
    stateSet=[[]]
    for i in range(processSize):#for each process
        newStateSet=[]
        for j in range(len(computation.processes[i].events)):# add 
            for k in range(len(stateSet)):
                tempS=stateSet[k]+[computation.processes[i].events[j].id]
                newStateSet.append(tempS)
        stateSet=newStateSet
    #check whether a state is consitent
    consistentStateSet=[]
    senderInfo=[]#two dim array senderInfo[i,j] means the senders so far on events j on pi
    for p in computation.processes:
        senderInfo.append([])
        curSender=[]
        for e in p.events:
            if e.status==eventStatus.RECEIVE:
                curSender.append(e.sender)
            senderInfo[-1].append(copy.deepcopy(curSender))
    for s in stateSet:
        if isConsistent(s,senderInfo):
            consistentStateSet.append(s)
    return consistentStateSet

def isUncomparable(state1,state2):
    isLarger=False
    isSmaller=False
    for i in range(len(state1)):
        if state1[i]>state2[i]:
            isLarger=True
        if state1[i]<state2[i]:
            isSmaller=True
    return isLarger and isSmaller

def stateInSlice(slice,state):
    #compute whether a state is a consistent global state in a slice
    for s in slice:
        if isUncomparable(s,state):
            return False
    return True

def maxCutIn(slice):
    #return max cut in slice
    ret=list(list(slice.keys())[0])
    for s in slice:
        for i in range(len(s)):
            ret[i]=max(ret[i],s[i])
    return ret

def minCutIn(slice):
    #return min cut in slice
    ret=list(list(slice.keys())[0])
    for s in slice:
        for i in range(len(s)):
            ret[i]=min(ret[i],s[i])
    return ret

def getConsistentStateOfSlice(slice):
    minS=minCutIn(slice)
    maxS=maxCutIn(slice)
    processSize=len(list(slice.keys())[0])
    stateSet=[[]]
    for i in range(processSize):#for each process
        newStateSet=[]
        for j in range(minS[i],maxS[i]+1):# for all possible eventid
            for k in range(len(stateSet)):
                tempS=stateSet[k]+[j]
                newStateSet.append(tempS)
        stateSet=newStateSet
    return stateSet