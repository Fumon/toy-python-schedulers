from process import RunningProcess

class Scheduler:
    cyclesRunning: int

    def __init__(self) -> None:
        self.cyclesRunning = 0

    def schedule(self, cycle: int, procs: dict[int, RunningProcess]) -> dict[int, RunningProcess]:
        pass