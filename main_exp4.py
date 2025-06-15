#( 
#python3 <<'EOF'
from qiskit.circuit.library import QFT
from GenParallelPool import GenParallelPool
from utils import *

from GeneradorCircuitsQuanticsExp4 import GeneradorCircuitsQuanticsExp4


gen_p = GenParallelPool(verbose=True)

# EXPERIMENT 4 #


number_circuits = 40



circuits = {
    "qft" : {
        "ratio_descent_gates_to_reorder": 1.9,
        "gates_to_reorder_min_percentatge": 0.04,
        "alpha": 0.99,
        "val": 2e-4
    },

    #"QPE" : {
    #    "ratio_descent_gates_to_reorder": 1.9,
    #    "gates_to_reorder_min_percentatge": 0.04,
    #    "temperature": 0.001,
    #    "alpha": 0.9
    #}
}
for t in [0.01]:
    for n_qubits in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]:

        for circ, data_circuit in circuits.items():
            #Circuit original


                qc_original=transpile_1_2_qgates(get_circuit(circ, n_qubits))
                probabilities = get_probabilities_for_gate(qc_original)
                desired_dist_gates_per_slice= get_histogram_gates_per_slice(qc_original)

                data = {
                    "number_of_gates": len(qc_original),
                    "desired_depth": qc_original.depth(),
                    "probabilities": probabilities,
                    "desired_dist_gates_per_slice": desired_dist_gates_per_slice,
                    "temperature": t,
                }

                for k, v in data_circuit.items():
                    data[k] = v

                method = "HC" if data["temperature"] == 0 else "SS"

                gen_p.generate_circuits(
                    custom_name=f"{circ}/exp4/{method}_q{n_qubits}",
                    generator=GeneradorCircuitsQuanticsExp4, number_circuits=number_circuits,
                    qc_original=qc_original,
                    data=data)

gen_p.execute(cores=16)

#EOF
#)  > out.txt 2>&1 & disown
