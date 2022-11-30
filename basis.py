from slice import getSlice,buildGraph,stateInSlice,maxCutIn,getConsistentStateOfSlice,getConsistentStates
from computation import eventStatus,computation,event,process
from predicate import operator
def getBasis(comp,predicate):
    ret=[]
    if predicate.isLocal:
        slice=getSlice(comp,predicate.subPredicate1)
        ret=[[slice,[]]]
    elif predicate.op==operator.DISJUNCTION:
        retP=getBasis(comp,predicate.subPredicate1)
        retQ=getBasis(comp,predicate.subPredicate2)
        ret.extend(retP)
        for r in retQ:
            if r in ret:
                continue
            else:
                ret.append(r)
    elif predicate.op==operator.CONJUNCTION:
        retP=getBasis(comp,predicate.subPredicate1)
        retQ=getBasis(comp,predicate.subPredicate2)
        for p in retP:
            for q in retQ:
                ret.append([getConjunctionOfSlice(p[0],q[0]),list(set(p[1]) | set(q[1]))])
    elif predicate.op==operator.EF: 
        #get maximum cut of slice and remove other
        sp=getBasis(comp,predicate.subPredicate1)
        for g in sp:
            ret.append([getEFOfSlice(g[0],comp),[]])
    else:#neg of ef           
        sp=getBasis(predicate.subPredicate1)
        item=[comp,[]]#todo: transform computation to slice by using always true predicate
        for g in sp:
            item[1].append(maxCutIn(g[0]))
        ret.append(item)
    nonEmptyRet=[]
    for r in ret:
        if r[0]!=dict() or r[1]!=[]:
            nonEmptyRet.append(r)
    return nonEmptyRet

def getConjunctionOfSlice(p,q):
    consistentStateP=getConsistentStateOfSlice(p)
    consistentStateQ=getConsistentStateOfSlice(q)
    stateSet=[]
    for state in consistentStateP:
        if state in consistentStateQ:
            stateSet.append(state)
    #transform state set to slice
    newSlice=buildGraph(stateSet)
    return newSlice

def getEFOfSlice(slice,comp):
    maximumCut=maxCutIn(slice)
    processes=[]
    for i in range(len(comp.processes)):
        processes.append(process(i,[]))
        for j in range(len(comp.processes[i].events)):
            if comp.processes[i].events[j].id<=maximumCut[i]:
                processes[i].events.append(comp.processes[i].events[j])
    newComputation=computation(processes)
    def truePredicate(state,comp):
        return True
    s=getSlice(newComputation,truePredicate)
    return s

def stateSatisfyPredicate(state,basis):
    for item in basis:
        #check state in slice
        if not stateInSlice(item[0],state):
            continue
        #check state in stable state
        stateInStableStructure=True
        for maxCut in item[1]:#ensure that item is larger thatn maxCut
            if item==maxCut:
                stateInStableStructure=False
                break
            for i in range(len(state)):
                if state[i]<maxCut[i]:#ensure every number is larger or equal
                    stateInStableStructure=False
        if stateInStableStructure:
            return True
    return False