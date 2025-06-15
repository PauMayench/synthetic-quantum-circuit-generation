# Quantum Circuit Generator

This project implements a quantum circuit generator capable of producing synthetic circuits that replicate both the **spatial** and **temporal** properties of known quantum algorithms. The goal is to enable more comprehensive benchmarking, testing, and training scenarios in quantum computing research.

## Overview

Current quantum circuit benchmarks are limited and do not represent the wide range of possible quantum architectures. Random circuits often lack structure, making them less useful for realistic performance evaluation. This generator addresses that gap by:

- **Sampling from the interaction graph** of an original quantum circuit to capture spatial relationships.
- **Applying a Simulated Annealing algorithm** guided by a loss function to mimic temporal properties such as gate depth and gate-per-slice distribution.

## Features

- Clone circuits like QFT, QPE, AE, and DJ with up to 100 qubits.
- Use Hill Climbing or Simulated Annealing with configurable parameters.
- Generate synthetic circuits from statistical or graph-based inputs (future extension).

## Parameters

The generator uses several tunable parameters:

| Parameter         | Description                                                               |
|-------------------|---------------------------------------------------------------------------|
| `OP_min`          | Minimum proportion of gates to reorder in one operator application.       |
| `OP_ratio`        | Rate at which the reorder size shrinks over iterations.                   |
| `T_initial`       | Initial temperature for Simulated Annealing.                              |
| `alpha`           | Cooling rate applied to temperature each iteration batch.                 |
| `val`             | Statistical convergence threshold based on sample mean and variance.      |

## Example Results

- For QFT, best results were achieved with `OP_ratio = 1.9`, `OP_min = 0.04`, `T_initial = 0.01`, and `alpha = 0.99`.
- Similar patterns were observed across other circuits like QPE, AE, and DJ.
- The generator consistently reduced loss and circuit depth while maintaining realistic gate distributions.


## Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/PauMayench/synthetic-quantum-circuit-generation.git
   cd synthetic-quantum-circuit-generation
   ```
2. Install dependencies
   ```bash
    pip install -r requirements.txt
   ```
  
  qiskit==1.3.2
  networkx==3.4.2


## Usage
  Update the desired parameters inside main.py adn then execute it with:
  ```bash
    python3 main.py
   ```

## New circuits
  To generate from other circuits thatn the ones implemented, just add them into circuits_originals/MQTbench
  and then edit utils.py.
> **Note:** Circuits can be downloaded from MQTbench: https://www.cda.cit.tum.de/mqtbench/


## References

- Quetschlich, Nils; Burgholzer, Lukas; Wille, Robert. “MQT Bench: Benchmarking Software and Design Automation Tools for Quantum Computing.” *Quantum*, 2023. Available at https://www.cda.cit.tum.de/mqtbench/  

## Acknowledgements

This work was developed as a Bachelor’s Thesis at FIB-UPC, with special thanks to:

- **Sergi Abadal** (Supervisor)  
- **Pau Escofet** and **Miquel Carrasco** (Co-Directors)  
- **My family and friends**, for their encouragement and support throughout this journey  

This work would not have been possible without their support.
