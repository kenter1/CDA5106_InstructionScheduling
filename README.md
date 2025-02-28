# Dynamic Instruction Scheduling Simulator
**CDA5106 Group 10**


## Description
A simulator for an out-of-order superscalar processor based on Tomasulo’s algorithm that fetches, dispatches, and issues N instructions per cycle. Only the dynamic scheduling mechanism was modeled, i.e., perfect caches and perfect branch prediction are assumed.

## Getting Started
To run this simulator, simply clone this repo and then run 

`python3 Simulator.py <S> <N> <tracefile>`

where `<S>` is the Scheduling Queue size, `<N>` is the peak fetch and dispatch rate, issue rate
will be up to N+1 and `<tracefile>` is the filename of the input trace.

It is written in python so `make` is not needed.

## Simulator Inputs
The simulator reads a trace file in the following format:

`<PC> <operation type> <dest reg #> <src1 reg #> <src2 reg #>`

Where
- `<PC>` is the program counter of the instruction (in hex).
- `<operation type>` is either “0”, “1”, or “2”.
- `<dest reg#>` is the destination register of the instruction. If it is -1, then the instruction does not have a destination register (for example, a conditional branch instruction). Otherwise, it is between 0 and 127.
- `<src1 reg #>` is the first source register of the instruction. If it is -1, then the instruction does not have a first source register. Otherwise, it is between 0 and 127.
- `<src2 reg #>` is the second source register of the instruction. If it is -1, then the instruction does not have a second source register. Otherwise, it is between 0 and 127.

**Group Members**
- Mark Kenneth Alano
- Timothy Callinan
- Carlos Caro
- Luis Galvis
- Yash Gharat
- Nicholas L'Heureux
- Jeremy Kim
