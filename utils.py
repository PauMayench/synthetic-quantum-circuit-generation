from qiskit import transpile

from qiskit.circuit.library import QFT, CDKMRippleCarryAdder
from qiskit import QuantumCircuit

import traceback


def get_circuit_from_qasm(name):
    return QuantumCircuit.from_qasm_file(f"original_circuits/MQTBench/{name}")


def get_circuit(nom, qubits):
    circuits = {
        "qft":      QFT,
        "AE":       f"ae_indep_qiskit_{qubits}.qasm",
        "DJ":       f"dj_indep_qiskit_{qubits}.qasm",
        #"Grover":   f"grover-v-chain_indep_qiskit_{qubits}.qasm",
        "QPE":      f"qpeexact_indep_qiskit_{qubits}.qasm",
        "adder":    CDKMRippleCarryAdder,
    }

    circ = circuits[nom]

    if isinstance(circ, str):
  
        return get_circuit_from_qasm(circ)
    
    if "adder" == nom:
        return circ(int(qubits/2 -1))
    return circ(qubits)

def transpile_1_2_qgates(qc):
    """
    transpiles the circuit with 1 and 2 qubit gates
    """

    two_qubit_gates = ['cx', 'cz', 'cp']
    single_qubit_gates = ['id', 'u1', 'u2', 'u3', 'x', 'y', 'z', 'h', 's', 'sdg', 't', 'tdg']

    return transpile(qc, basis_gates=single_qubit_gates+two_qubit_gates, optimization_level=0)



def get_probabilities_for_gate(circuit):
    """
    Returns the probabilities for each gate to be on the given circuit (normalized adjacency matrix)
    Input: QuantumCircuit
    Output: 
        - dict: A dictionary mapping a qubit index (for one-qubit gates) or a tuple of qubit indices 
        (for two-qubit gates) to the normalized probability of that gate being applied in the circuit.

    """
    gate_count = {}

    total = 0

    for gate in circuit.data:

        if gate.operation.num_qubits == 1:
            qbit = gate.qubits[0]._index
            gate_count[qbit] = gate_count.get(qbit, 0) +1
            total += 1
        elif gate.operation.num_qubits == 2:
            qbit1 = gate.qubits[0]._index
            qbit2 = gate.qubits[1]._index
            if qbit1 == qbit2:
                gate_count[qbit1] = gate_count.get(qbit1, 0) +1
                total += 1
                continue
            g = (max(qbit1 , qbit2), min(qbit1 , qbit2))
            gate_count[g] = gate_count.get(g, 0) + 1
            total += 1
        else:
           print("Transpile the circuit to 1 and 2 based qubit gates")
        
    for k in gate_count.keys():
        gate_count[k] = gate_count[k]/total
    return gate_count



from qiskit import *
from qiskit.circuit.library import QFT
import networkx as nx
import numpy as np
import time

from qiskit.transpiler import PassManager, CouplingMap
from qiskit.transpiler.passes import SabreSwap, TrivialLayout, SabreLayout
import random


## METRICS #################################

def get_adj_matrix(circuit):
    gate_count = {}

    total = 0

    for gate in circuit.data:

        if gate.operation.num_qubits == 1:
            qbit = gate.qubits[0]._index
            gate_count[qbit] = gate_count.get(qbit, 0) +1
            total += 1
        elif gate.operation.num_qubits == 2:
            qbit1 = gate.qubits[0]._index
            qbit2 = gate.qubits[1]._index
            if qbit1 == qbit2:
                gate_count[qbit1] = gate_count.get(qbit1, 0) +1
                total += 1
                #print("LIADA")
                continue
            g = (max(qbit1 , qbit2), min(qbit1 , qbit2))
            gate_count[g] = gate_count.get(g, 0) + 1
            total += 1
        else:
           print("Transpile the circuit to 1 and 2 based qubit gates")

    return gate_count

def evaluate_circuit_metrics(qc_original, qc_to_evaluate):

    h1 = get_histogram_gates_per_slice(qc_original)
    h2 = get_histogram_gates_per_slice(qc_to_evaluate)

    #normalitzem h
    s1 = sum(v for v in h1.values())
    s2 = sum(v for v in h2.values())

    h1= {k:v/s1 for k,v in h1.items()}
    h2= {k:v/s2 for k,v in h2.items()}
    #


    res = sum(abs(h1[k] - h2.get(k, 0)) for k in h1.keys())
    res += sum(h2[k] for k in h2.keys() if k not in h1.keys())

    res /= 2

    d = qc_to_evaluate.depth()
    try:
        compiled = get_metrics(qc_to_evaluate)
        comp_d = compiled["depth"]
        s = compiled["swaps"]
    except Exception:
        print("Could not compile, error:")        
        traceback.print_exc()

        comp_d = None 
        s = None


    ad1 = get_probabilities_for_gate(qc_original)
    ad2 = get_probabilities_for_gate(qc_to_evaluate)
    
    #print([ad1[k] - ad2.get(k, 0) for k in ad1.keys()][:10])

    diff_ad = sum(abs(ad1[k] - ad2.get(k, 0)) for k in ad1.keys())
    diff_ad += sum(abs(-ad2[k]) for k in ad2.keys() if k not in ad1.keys())

    diff_ad /= 2

    #suma_original = sum(abs(ad1[k]) for k in ad1.keys())
    #suma_generat = sum(ad2.get(k, 0) for k in ad1.keys())
    #print(f"{suma_original} {suma_generat}")


    return {"Depht": d, "Compiled Depht": comp_d, "Difference Distribution Gates per Slice": res, "Swaps": s, "Difference Adjacency Matrix": diff_ad}










################################################

def get_data_generic(qc_original, qc_to_evaluate):

    #h1 = get_histogram_gates_per_slice(qc_original)
    #h2 = get_histogram_gates_per_slice(qc_to_evaluate)

    #res = sum(abs(h1[k] - h2.get(k, 0)) for k in h1.keys())
    #res += sum(h2[k] for k in h2.keys() if k not in h1.keys())


    #d = qc_to_evaluate.depth()

    compiled = get_metrics(qc_to_evaluate)
    d = compiled["depth"]
    #d = compiled["swaps"]

    return {"metr": d}



def get_metrics_circuit(qc):
    #qc2 = transpile_1_2_qgates(qc)
    depth = qc.depth()
    hist = get_histogram_gates_per_slice(qc)
    return {"depth": depth, "hist": hist}


def get_metrics_bo(circ, qubits = 100):


     # 10x10 grid

    # Create a grid graph representing the connectivity of the quantum processor
    G = nx.grid_2d_graph(int(np.sqrt(qubits)), int(np.sqrt(qubits)))
    A = nx.adjacency_matrix(G).toarray()

    adj_list = []
    for i in range(len(A)):
        for j in range(len(A[0])):
            if A[i][j] == 1:
                adj_list.append([i, j])

    #pos = {n:n for n in G.nodes()}
    #edge_fidelity = {e:1.0 for e in G.edges()} # edge fidelity of 1 in all edges
    #edge_error_rate = {e:1-edge_fidelity[e] for e in G.edges()}
    #nx.set_node_attributes(G, pos, 'pos')

    coupling_map = CouplingMap(adj_list)

    # Routing and Initial Placement strategies
    routing = SabreSwap(coupling_map=coupling_map, trials=1, heuristic='basic')
    placement = TrivialLayout(coupling_map=coupling_map)
    # sabre_placement = SabreLayout(coupling_map=coupling_map)

    pm = PassManager([placement, routing])
    init_time = time.monotonic()
    compiled_circuit = pm.run(circ)
    exec_time = time.monotonic() - init_time
    depth = compiled_circuit.depth()

    #print('SWAP gates:', compiled_circuit.count_ops()['swap'])
    #print('Resulting depth:', depth)
    #print('Execution time:', exec_time)
    return {"depth": depth, "swaps": compiled_circuit.count_ops()['swap']}

def get_metrics(circ, qubits = 100):


     # 10x10 grid

    # Create a grid graph representing the connectivity of the quantum processor
    G = nx.grid_2d_graph(int(np.sqrt(qubits)), int(np.sqrt(qubits)))
    A = nx.adjacency_matrix(G).toarray()

    adj_list = []
    for i in range(len(A)):
        for j in range(len(A[0])):
            if A[i][j] == 1:
                adj_list.append([i, j])

    coupling_map = CouplingMap(adj_list)

    compiled_circuit = transpile(
        circ,
        coupling_map=coupling_map,
        initial_layout=list(range(qubits)),      # trivial: virtual i → physical i
        routing_method='sabre',
        optimization_level=0
    )

    depth = compiled_circuit.depth()

    #print('SWAP gates:', compiled_circuit.count_ops()['swap'])
    #print('Resulting depth:', depth)
    #print('Execution time:', exec_time)
    return {"depth": depth, "swaps": compiled_circuit.count_ops()['swap']}



from qiskit.converters import circuit_to_dag


def get_histogram_gates_per_slice(qc):
    """
    Computes the histogram of gates per slice in a quantum circuit.
        Parameters:
        qc (QuantumCircuit): The quantum circuit to analyze.

    Returns:
        dict: A dictionary  dict[n gates]=number of slices that have n gates
    """


    dag = circuit_to_dag(qc)
    layers = dag.layers()
    density_per_slice = [len(layer["partition"]) for layer in layers]

    dist = {}
    for n_gates in density_per_slice:
        dist[n_gates] = 1 + dist.get(n_gates, 0)


    return dist