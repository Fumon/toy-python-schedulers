from enum import Enum
from pathlib import PurePath
from sys import stdout
from process import Process

import argparse
from sched.fcfs import FCFS
from sched.roundrobin import RoundRobin
from sched.shortestjobfirst import SJF

from sim import Simulator

class Algorithms(Enum):
    FCFS = '0'
    RR = '1'
    SJF = '2'

    def help(self) -> str:
        return {
            Algorithms.FCFS.name: "First Come First Serve",
            Algorithms.RR.name: "Round Robin",
            Algorithms.SJF.name: "Shortest Job First"
        }[self.name]
        

parser = argparse.ArgumentParser(description='Run a scheduler Example')
parser.add_argument('procfile', metavar='FILENAME', type=str)
parser.add_argument('algo', type=str, choices=list(a.value for a in Algorithms), help='\n'.join(f"{a.value}: {a.help()}" for a in Algorithms))
parser.add_argument('--stdout', action=argparse.BooleanOptionalAction, dest='stdout', default=False, type=bool, help="output to stdout instead of a file", )

args = parser.parse_args()


with open(args.procfile, 'r') as f:
    num: int = int(f.readline())
    procs: list[Process] = [Process.fromLine(line) for line in [f.readline() for x in range(num)]]


if args.stdout:
    output = stdout
else:
    path = PurePath(args.procfile)
    output = open(path.parent.parent / "output" / (path.stem + f"-{args.algo}.txt"), 'w')

match Algorithms(args.algo):
    case Algorithms.RR:
        Simulator(RoundRobin(2), procs, output=output).run()
    case Algorithms.FCFS:
        Simulator(FCFS(), procs, output=output).run()
    case Algorithms.SJF:
        Simulator(SJF(), procs, output=output).run()

output.close()