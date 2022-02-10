from collections import deque
from process import RunningProcess, Status
from sched.scheduler import Scheduler



class RoundRobin(Scheduler):
    quantum: int
    queue: deque[int]
    
    def __init__(self, quantum: int) -> None:
        super().__init__()
        self.quantum = quantum
        self.queue = deque([])
    
    def schedule(self, cycle: int, procs: dict[int, RunningProcess]) -> dict[int, RunningProcess]:

        # Enqueue procs which are READY but not already in the queue
        match [pid for pid, proc in procs.items()\
            if (pid not in self.queue) and (proc.curStatus == Status.READY)]:
            case [readypid]: # Only one
                self.queue.append(readypid)
            case newreadies:
                # Sort by pid
                newreadies.sort()
                self.queue.extend(newreadies)
        
        # Find running procs
        match [[pid, self.quantum > (cycle - proc.runningSince)] for pid, proc in procs.items()
            if proc.curStatus == Status.RUNNING]:
            case [[_, _], *c] if len(c) > 0:
                # ERROR more than one process running
                raise RuntimeError('More than one process in RUNNING state', procs)
            case [[rpid, False]]:
                if len(self.queue):
                    # Quantum has passed and we have a process waiting
                    procs[rpid] = procs[rpid].preempt()
                else:
                    self.cyclesRunning += 1
                    return procs
            case [[rpid, True]]:
                # Quantum has not passed. Do nothing and return current procs
                self.cyclesRunning += 1
                return procs
        
        # If we have a ready process, start it
        if len(self.queue):
            npid = self.queue.popleft()
            procs[npid] = procs[npid].run(cycle)
            self.cyclesRunning += 1

        return procs
