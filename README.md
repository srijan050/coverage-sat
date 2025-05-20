# Coverage-Driven Verification using SAT Solver

## Overview

This repository implements the PLNSAT (Property List Narrowing SAT) algorithm described in the research paper titled "Efficient Coverage-Driven Stimulus Generation Using Simultaneous SAT Solving, with Application to SystemVerilog." PLNSAT leverages Boolean SAT solving to generate stimuli that fulfill coverage bins defined in SystemVerilog covergroups. It translates functional coverage points into CNF (Conjunctive Normal Form) using Tseitin Transformation, enabling efficient solving of complex verification tasks.


## Implementation Details

### Tseitin Transformation

* Translates complex logical expressions from SystemVerilog modules and bins into CNF efficiently. Read about it [here](https://en.wikipedia.org/wiki/Tseytin_transformation)

### Coverage Bins

* Each variable is defined with bins representing possible values, an example for three variables :

  ```
  Variable 'a': {0}, {1}
  Variable 'b': {0}, {1}
  Variable 'y': {0}, {1}
  ```

### Example

#### AND Gate

Variables:

* `a = 1`, `b = 2`, `y = 3`

CNF representation of `(a & b) ↔ y`:

```cnf
[[-1, 3],
 [-2, 3],
 [-3, 1, 2]]
```

#### OR Gate

Variables:

* `a = 1`, `b = 2`, `y = 3`

CNF representation of `(a | b) ↔ y`:

```cnf
[[-1, 3],
 [-2, 3],
 [-3, 1, 2]]
```

Bin clauses:

```cnf
[[1]],  # a = 1
[[-1]], # a = 0
[[2]],  # b = 1
[[-2]], # b = 0
[[3]],  # y = 1
[[-3]]  # y = 0
```

## Output

The generated stimuli satisfying coverage conditions are stored in:

```
stimuli.mem
```

## Setup and Usage

Make sure you have "pysat" installed for the solver:

```
pip install pysat
```
Clone this repository:

```bash
git clone <repository-url>
cd <repository-folder>
```

Run the SAT solver for your desired module and bins:

```
python plnsat_solver.py
```

## Testing and Examples

Additional gate examples for testing can be found [here](https://en.wikipedia.org/wiki/Tseytin_transformation#Gate_sub-expressions) like:

* XOR Gate
* NAND Gate
* NOR Gate

<img width="781" alt="image" src="https://github.com/user-attachments/assets/51049aea-7950-46c7-bc8f-9acd42bb8fd8" />


## Future Work

* Automate CNF generation instead of current manual definitions.
* Extend to more complex sequential circuits.
* Integrate more comprehensive SystemVerilog constructs.

## References

* An-Che Cheng, Chia-Chih (Jack) Yen, Celina G. Val, Sam Bayless, Alan J. Hu, Iris Hui-Ru Jiang, and
Jing-Yang Jou. 2014. Efficient coverage-driven stimulus generation using simultaneous SAT solving, with
application to systemVerilog. ACM Trans. Des. Autom. Electron. Syst. 20, 1, Article 7 (November 2014), 23
pages.
DOI: http://dx.doi.org/10.1145/2651400

---
