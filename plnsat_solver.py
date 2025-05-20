# plnsat_solver.py
#!/usr/bin/env python3
"""
Generic PLNSAT stimulus generator using python-sat.
Encodes both the circuit CNF and per-bin CNFs, then runs
the PLNSAT loop to hit every bin with as few tests as possible.
Writes `stimuli.mem` (binary a b) for tb_simple_and.sv.
"""

from pysat.solvers import Solver

class PLNSATSolver:
    def __init__(self, num_vars, circuit_cnf, bins_cnf):
        self.num_vars    = num_vars
        self.circuit_cnf = circuit_cnf[:]    # CNF for circuit
        self.bins_cnf    = bins_cnf[:]       # list of per-bin CNFs
        self.tests       = []

    def solve(self):
        remaining = list(range(len(self.bins_cnf)))
        while remaining:
            with Solver(name='m22') as solver:
                # always enforce the circuit behavior
                for clause in self.circuit_cnf:
                    solver.add_clause(clause)

                # add selector vars for each remaining bin
                sel_off   = self.num_vars
                selectors = []
                for idx, b in enumerate(remaining):
                    s = sel_off + idx + 1
                    selectors.append(s)
                    # guard each bin's clauses under ¬s → clause
                    for clause in self.bins_cnf[b]:
                        solver.add_clause([-s] + clause)

                # force at least one selector true
                solver.add_clause(selectors)

                if not solver.solve():
                    raise RuntimeError(f"No assignment covers any of bins {remaining}")

                model = solver.get_model()

            # extract full assignment
            assign = [1 if model[i-1] > 0 else 0
                      for i in range(1, self.num_vars+1)]
            self.tests.append(assign)

            # remove every bin now satisfied
            covered = [b for b in remaining
                       if self._satisfies(self.bins_cnf[b], assign)]
            for b in covered:
                remaining.remove(b)

        return self.tests

    def _satisfies(self, cnf, assign):
        # every clause must be true under `assign`
        for clause in cnf:
            if not any((lit>0 and assign[abs(lit)-1]==1)
                       or (lit<0 and assign[abs(lit)-1]==0)
                       for lit in clause):
                return False
        return True

# This example generates a test for the circuit of a simple AND gate
# (a & b) ↔ y, with bins according to the testbench : tb_simple_and.sv
# a = [0,1], b = [0,1], y = [0,1]


if __name__ == '__main__':
    # Variables: 1=a, 2=b, 3=y
    num_vars = 3

    # (a & b) ↔ y in CNF:
    circuit_cnf = [[1, -3],
                   [2, -3],
                   [3, -1, -2]]


    # exact-assignment bins (unit clauses) for all bins :
    bins_cnf = [
        [[1]], # a = 1
        [[-1]], # a = 0
        [[2]], # b = 1
        [[-2]], # b = 0
        [[3]], # y = 1
        [[-3]], # y = 0
    ]

    solver = PLNSATSolver(num_vars, circuit_cnf, bins_cnf)
    full_tests = solver.solve()

    # write only input vectors to stimuli.mem
    with open('stimuli.mem','w') as f:
        for t in full_tests:
            tmp = t[:-1]  # remove y
            f.write(''.join(map(str, tmp)) + '\n')

    print("Generated stimuli.mem:")
    for t in full_tests:
        print(t[:-1])
