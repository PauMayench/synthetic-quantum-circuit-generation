#( 
#python3 <<'EOF'
from qiskit.circuit.library import QFT
from GenParallelPool import GenParallelPool
from utils import *

from GeneradorCircuitsQuanticsExp2 import GeneradorCircuitsQuanticsExp2


gen_p = GenParallelPool(verbose=True)

# EXPERIMENT 2 #

qubits = 100
number_circuits = 15



circuits = {
    #"qft" : {
    #    "val": 1e-6,
    #    "ratio_descent_gates_to_reorder":1.3, #1.1,  #1.9,              #1.6,#1.2, #1.6,
    #    "gates_to_reorder_min_percentatge":0.32, #0.04,#0.04            #0.08  #0.64# 0.32
    #},
    #"QPE" : {
    #    "val": 1e-6,
    #    "ratio_descent_gates_to_reorder": 1.5,#1.9,  #1.1,
    #    "gates_to_reorder_min_percentatge": 0.64#0.04, #0.16
    #}
    #"AE" : {
    #    "val": 1e-6,
    #    "ratio_descent_gates_to_reorder": 1.7, #1.2,
    #    "gates_to_reorder_min_percentatge": 0.08#0.08
    #},
    "DJ" : {
        "val": 1e-6,
        "ratio_descent_gates_to_reorder": 2,
        "gates_to_reorder_min_percentatge": 0.32
    }


}

temps = [0.1, 0.01, 0.001, 0.0001]
alphs = [0.99, 0.95, 0.9, 0.85, 0.8]

for circ, data_circuit in circuits.items():
    #Circuit original
    for temp in temps:
        for alpha in alphs:

            qc_original=transpile_1_2_qgates(get_circuit(circ, qubits))
            probabilities = get_probabilities_for_gate(qc_original)
            desired_dist_gates_per_slice= get_histogram_gates_per_slice(qc_original)

            data = {
                "number_of_gates": len(qc_original),
                "desired_depth": qc_original.depth(),
                "probabilities": probabilities,
                "desired_dist_gates_per_slice": desired_dist_gates_per_slice,
                
                "temperature": temp,
                "alpha": alpha
            }

            for k, v in data_circuit.items():
                data[k] = v


            gen_p.generate_circuits(
                custom_name=f'{circ}/exp2_{data_circuit["ratio_descent_gates_to_reorder"]}_{data_circuit["gates_to_reorder_min_percentatge"]}/t{temp}_a{alpha}',
                generator=GeneradorCircuitsQuanticsExp2, number_circuits=number_circuits,
                qc_original=qc_original,
                data=data)

gen_p.execute(cores=15)

#EOF
#)  > out_AE_Exp2.txt 2>&1 & disown