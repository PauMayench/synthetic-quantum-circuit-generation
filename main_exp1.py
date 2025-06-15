#( 
#python3 <<'EOF'
from qiskit.circuit.library import QFT
from GenParallelPool import GenParallelPool
from utils import *

from GeneradorCircuitsQuanticsExp1 import GeneradorCircuitsQuanticsExp1


gen_p = GenParallelPool(verbose=True)

# EXPERIMENT 1 #

qubits = 100
number_circuits = 15



circuits = {
    "adder" : {
    }
}

#ratios = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2]
ratios = [2, 1.9, 1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2, 1.1]
min_percentages = [0.04, 0.08, 0.16, 0.32, 0.64, 1.28, 2.56, 5.12, 10.24, 20.48] # [0.04*2**i for i in range(0,10)]


for circ, data_circuit in circuits.items():
    #Circuit original
    for ratio_desc in ratios:
        for min_percent in min_percentages:
            print(circ)
            qc_original=transpile_1_2_qgates(get_circuit(circ, qubits))
            probabilities = get_probabilities_for_gate(qc_original)
            desired_dist_gates_per_slice= get_histogram_gates_per_slice(qc_original)
            data = {
                "number_of_gates": len(qc_original),
                "desired_depth": qc_original.depth(),
                "probabilities": probabilities,
                "desired_dist_gates_per_slice": desired_dist_gates_per_slice,
                
                "ratio_descent_gates_to_reorder": ratio_desc,
                "gates_to_reorder_min_percentatge": min_percent
            }

            for k, v in data_circuit.items():
                data[k] = v


            gen_p.generate_circuits(
                custom_name=f"{circ}/exp1/ratio{ratio_desc}_min{min_percent}",
                generator=GeneradorCircuitsQuanticsExp1, number_circuits=number_circuits,
                qc_original=qc_original,
                data=data)

gen_p.execute(cores=15)

#EOF

#)  > out.txt 2>&1 & disown