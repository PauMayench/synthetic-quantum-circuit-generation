#( 
#python3 <<'EOF'
from qiskit.circuit.library import QFT
from GenParallelPool import GenParallelPool
from utils import *

from GeneradorCircuitsQuanticsExp3 import GeneradorCircuitsQuanticsExp3


gen_p = GenParallelPool(verbose=True)

# EXPERIMENT 3 #

qubits = 100
number_circuits = 50



circuits = {
    "qft" : {
        "ratio_descent_gates_to_reorder": 1.6,
        "gates_to_reorder_min_percentatge": 0.08,
        "temperature": 0.01,
        "alpha": 0.99
    },
    #"QPE" : {
    #    "ratio_descent_gates_to_reorder": 1.9,
    #    "gates_to_reorder_min_percentatge": 0.04,
    #    "temperature": 0.001,
    #    "alpha": 0.9
    #}
}

val = 1e-7
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
            "val": val

        }

        for k, v in data_circuit.items():
            data[k] = v


        gen_p.generate_circuits(
            custom_name=f"{circ}/exp3/v{val}",
            generator=GeneradorCircuitsQuanticsExp3, number_circuits=number_circuits,
            qc_original=qc_original,
            data=data)

gen_p.execute(cores=15)

#EOF
#)  > out.txt 2>&1 & disown
#
#
#) 2>&1 | tee out.txt & disown
