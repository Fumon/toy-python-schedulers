from process import RunningProcess, Status
from sched.scheduler import Scheduler

class SJF(Scheduler):
    def __init__(self) -> None:
        super().__init__()
    
    def schedule(self, cycle: int, procs: dict[int, RunningProcess]) -> dict[int, RunningProcess]:
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

        # Start the next proc with the lowest runtime if there's one READY
        match [proc for proc in procs.values() if proc.curStatus == Status.READY]:
            case [readyproc]: # Only one
                procs[readyproc.proc.pid] = readyproc.run(cycle)
                self.cyclesRunning += 1
            case readies if len(readies):
                # Sort by remaining run time and secondarily pid.
                readies.sort(key = lambda p : (p.proc.cpu_time - p.runcycles, p.proc.pid))
                nextReady = readies[0]

                procs[nextReady.proc.pid] = nextReady.run(cycle)
                self.cyclesRunning += 1
                
        
        return procs
