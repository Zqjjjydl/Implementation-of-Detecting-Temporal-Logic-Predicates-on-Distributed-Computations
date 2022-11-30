from enum import Enum
class operator(Enum):
    DISJUNCTION=0
    CONJUNCTION=1
    EF=2
    NEG=3


class predicate:
    def __init__(self,isLocal,subPred1,subPred2=None,op=None) -> None:
        self.op=op
        self.subPredicate1=subPred1
        self.subPredicate2=subPred2
        self.isLocal=isLocal#true if current predicate is a local one, in this case, only subPredicate1 will be meaningful 