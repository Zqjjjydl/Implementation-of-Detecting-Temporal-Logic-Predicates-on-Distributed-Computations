from enum import Enum
class eventStatus(Enum):
    SEND=0
    RECEIVE=1
    INTERNAL=2

class event:
    def __init__(self,id,value,status,sender=(-1,-1),receiver=(-1,-1)):
        self.id=id
        self.value=value
        self.status=status
        self.sender=sender#pid,eventid
        self.receiver=receiver#pid,eventid


class process:
    def __init__(self,pid,events):
        self.pid=pid
        self.events=events#array of event

class computation:
    def __init__(self,processes):
        self.processes=processes#array of process
        pass