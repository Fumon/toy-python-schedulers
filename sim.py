from io import TextIOWrapper
from sys import stdout
from typing import TextIO
from sched.scheduler import Scheduler
from process import Process, RunningProcess, Status
from collections import OrderedDict


PrintStatuses: set[Status] = {Status.READY, Status.RUNNING, Status.BLOCKED}
AllStatuses: set[Status] = set(list(Status))

class Simulator:
    cycle: int
    runningProcs: OrderedDict[int, RunningProcess]
    scheduler: Scheduler
    output: TextIOWrapper

    def __init__(self, scheduler, procs: list[Process], output: TextIOWrapper = stdout, startCycle: int = 0) -> None:
        self.cycle = startCycle
        self.scheduler = scheduler
        self.output = output

        procs.sort(key = lambda p : p.pid)

        self.runningProcs = OrderedDict((p.proc.pid, p) for p in [RunningProcess(p, startCycle) for p in procs])
    
    def run(self):
        self.clock()
        while all([p.curStatus == Status.FINISHED for p in self.runningProcs.values()]) == False:
            self.status()
            self.cycle += 1
            self.clock()
        
        self.statblock()
    
    def statblock(self):

        print("", file=self.output)
        print(f"Finishing time: {self.cycle - 1}", file=self.output)
        print(f"CPU utilization: {self.scheduler.cyclesRunning/self.cycle:.2f}", file=self.output)
        # I really loved this horrible oneliner, but I needed the pid so I just precomputed and settled for a generator
        #for turnaround in (p.finishedCycle - p.proc.arrival_time + 1 for p in self.runningProcs.values()):
        for [pid, turnaround] in ([pid, p.turnaround] for pid, p in self.runningProcs.items()):
            print(f"Turnaround process {pid}: {turnaround}", file=self.output)

    def status(self):
        statuses = ' '.join(f"{pid}:{p.curStatus.value}" for pid, p in self.runningProcs.items() if \
            p.curStatus in PrintStatuses)
        print(f"{self.cycle} {statuses}", file=self.output)

    def clock(self):
        self.runningProcs = {pid: p.clock(self.cycle) for pid, p in self.runningProcs.items()}
        self.runningProcs = self.scheduler.schedule(self.cycle, self.runningProcs)

        
