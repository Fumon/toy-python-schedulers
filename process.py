from __future__ import annotations
from enum import Enum

class Status(Enum):
    PREARRIVE = 'prearrive'
    READY = 'ready'
    RUNNING = 'running'
    BLOCKED = 'blocked'
    FINISHED = 'finished'

class Process:
    pid: int
    cpu_time: int
    io_time: int
    arrival_time: int

    run_time: int
    cpu_burst: int

    def __init__(self, pid: int, cpu_time: int, io_time: int, arrival_time: int) -> None:
        self.pid, self.cpu_time, self.io_time, self.arrival_time = \
            pid, cpu_time, io_time, arrival_time
        
        self.cpu_burst = cpu_time if io_time == 0 else cpu_time//2 + cpu_time % 2

        self.run_time = cpu_time if io_time == 0 else self.cpu_burst * 2 + io_time


    def fromLine(line: str) -> Process:
        s = [int(a) for a in line.split()]
        if(len(s) != 4):
            raise ValueError('Wrong number of vals for process')
        
        return Process(*s)

class RunningProcess:
    runcycles: int
    blockcycles: int

    runningSince: int
    turnaround: int

    proc: Process

    curStatus: Status

    def __init__(self, proc: Process, initCycle: int = 0) -> None:
        self.proc = proc

        self.runningSince = -1
        self.curStatus = Status.PREARRIVE if self.proc.arrival_time > initCycle else Status.READY
        self.runcycles = 0
        self.blockcycles = 0
        self.turnaround = 0
        
    def clock(self, curCycle: int) -> RunningProcess:
        match self.curStatus:
            case Status.RUNNING:
                self.runcycles += 1
            case Status.BLOCKED:
                self.blockcycles += 1
        
        self._update(curCycle)

        return self

    def _update(self, curCycle: int) -> None:
        match self.curStatus:        
            case Status.PREARRIVE:
                if self.proc.arrival_time <= curCycle:
                    self.curStatus = Status.READY
            case Status.READY:
                pass
            case Status.BLOCKED:
                self.curStatus = Status.BLOCKED if self.proc.io_time > self.blockcycles\
                    else Status.READY
            case Status.RUNNING:
                match [
                    self.proc.cpu_burst > self.runcycles,
                    self.proc.io_time > self.blockcycles,
                    self.proc.run_time > self.runcycles + self.blockcycles
                ]:
                    case [True, *_]:
                        pass
                    case [False, True, _]:
                        self.curStatus = Status.BLOCKED
                    case [False, False, False]:
                        self.curStatus = Status.FINISHED
                        self.turnaround = curCycle - self.proc.arrival_time
            case Status.FINISHED:
                pass
            
    def preempt(self) -> RunningProcess:
        match self.curStatus:
            case Status.RUNNING:
                self.runningSince = -1
                self.curStatus = Status.READY
        
        return self
    
    def run(self, cycle: int) -> RunningProcess:
        match self.curStatus:
            case Status.READY:
                self.runningSince = cycle
                self.curStatus = Status.RUNNING
        
        return self
