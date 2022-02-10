
from collections import deque
from process import RunningProcess, Status
from sched.scheduler import Scheduler



class FCFS(Scheduler):
    queue: deque[int]
    
    def __init__(self) -> None:
        super().__init__()
        self.queue = deque([])
    
    def schedule(self, cycle: int, procs: dict[int, RunningProcess]) -> dict[int, RunningProcess]:

        # Enqueue procs which are READY but not already in the queue
        match [pid for pid, proc in procs.items()\
            if (pid not in self.queue) and (proc.curStatus == Status.READY)]:
            case [readypid]:
                self.queue.append(readypid)
            case newreadies:
                # Sort by pid
                newreadies.sort()
                self.queue.extend(newreadies)
        
        # Find running procs
        match [pid for pid, proc in procs.items()
            if proc.curStatus == Status.RUNNING]:
            case [_, *c] if len(c) > 0:
                # ERROR more than one process running
                raise RuntimeError('More than one process in RUNNING state', procs)
            case [rpid]:
                # It's still running
                self.cyclesRunning += 1
                return procs
        
        # If we have a ready process, start it
        if len(self.queue):
            npid = self.queue.popleft()
            procs[npid] = procs[npid].run(cycle)
            self.cyclesRunning += 1

        return procs