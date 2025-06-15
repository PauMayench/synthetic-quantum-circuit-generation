#( 
#python3 <<'EOF'
from qiskit.circuit.library import QFT
from GenParallelPool import GenParallelPool
from utils import *

from GeneradorCircuitsQuantics import GeneradorCircuitsQuantics


gen_p = GenParallelPool(verbose=True)

# GENERACIO CIRUCITS #

qubits = 100
cores = 16

circuits = {
      
    "qft" : {
        "ratio_descent_gates_to_reorder": 1.9,
        "gates_to_reorder_min_percentatge": 0.04,
        "temperature": 0.01,
        "alpha": 0.99,
        "val": 1.5e-4,
        "number_circuits": 82
    },


    #"QPE" : {
    #    "ratio_descent_gates_to_reorder": 1.9,
    #    "gates_to_reorder_min_percentatge": 0.04,
    #    "temperature": 0.001,
    #    "alpha": 0.9,
    #    "val": 2e-4,
    #    "number_circuits": 100
    #},
    #"DJ" : {
    #    "ratio_descent_gates_to_reorder": 2,
    #    "gates_to_reorder_min_percentatge": 0.32,
    #    "temperature": 0.01,
    #    "alpha": 0.85,
    #    "val": 0.5e-4,
    #    "number_circuits": 100
    #},
    #"AE" : {
    #    "ratio_descent_gates_to_reorder": 1.1,
    #    "gates_to_reorder_min_percentatge": 0.04,
    #    "temperature": 0.001,
    #    "alpha": 0.85,
    #    "val": 2e-4,
    #    "number_circuits": 100
    #},
    #"adder" : {
    #    "ratio_descent_gates_to_reorder": 1.7,
    #    "gates_to_reorder_min_percentatge": 0.16,
    #    "temperature": 0.01,
    #    "alpha": 0.99,
    #    "val": 2e-4,
    #    "number_circuits": 100
    #}


}


for circ, data_circuit in circuits.items():
    #Circuit original


        qc_original=transpile_1_2_qgates(get_circuit(circ, qubits))
        probabilities = get_probabilities_for_gate(qc_original)
        desired_dist_gates_per_slice= get_histogram_gates_per_slice(qc_original)

        data = {
            "number_of_gates": len(qc_original),
            "desired_depth": qc_original.depth(),
            "probabilities": probabilities,
            "desired_dist_gates_per_slice": desired_dist_gates_per_slice,

        }

        for k, v in data_circuit.items():
            data[k] = v


        gen_p.generate_circuits(
            custom_name=f"{circ}/generate/v3",
            generator=GeneradorCircuitsQuantics, number_circuits=data_circuit["number_circuits"],
            qc_original=qc_original,
            data=data)

gen_p.execute(cores=cores)

#EOF
#)  > out.txt 2>&1 & disown