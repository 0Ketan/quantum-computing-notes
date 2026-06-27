'''
Quantum Phase Estimation (QPE) Example
This script demonstrates the Quantum Phase Estimation algorithm
for estimating the phase (eigenvalue) of a unitary operator.
We use a simple phase gate as the unitary U.
'''

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import numpy as np
import matplotlib.pyplot as plt

def run_qpe_example():
    # Example: Estimate the phase of a phase gate with angle theta = 2 * pi * 0.375
    # This corresponds to binary 0.011 (0.375 in decimal)
    theta = 2 * np.pi * 0.375  # angle in radians
    num_counting_qubits = 3
    
    # Create quantum circuit with counting qubits + 1 target qubit
    # and classical bits for measurement
    qc = QuantumCircuit(num_counting_qubits + 1, num_counting_qubits)
    
    # Step 1: Apply Hadamard to all counting qubits
    for q in range(num_counting_qubits):
        qc.h(q)
    
    # Step 2: Prepare the target qubit in |1> (eigenstate of phase gate)
    qc.x(num_counting_qubits)  # target qubit is the last one (index num_counting_qubits)
    
    # Step 3: Apply controlled-U^{2^k} operations
    # where U is the phase gate Rz(theta)
    for k in range(num_counting_qubits):
        power = 2 ** k
        angle = power * theta  # angle for U^{2^k}
        qc.cp(angle, k, num_counting_qubits)  # controlled-phase gate
    
    # Step 4: Apply inverse Quantum Fourier Transform (IQFT) on counting qubits
    # We'll implement IQFT manually for clarity
    # First, swap qubits to reverse order
    for i in range(num_counting_qubits // 2):
        qc.swap(i, num_counting_qubits - 1 - i)
    # Apply Hadamard and controlled phase rotations
    for j in range(num_counting_qubits):
        qc.h(j)
        for m in range(j):
            qc.cp(-np.pi / (2 ** (j - m)), m, j)
    
    # Step 5: Measure the counting qubits
    for q in range(num_counting_qubits):
        qc.measure(q, q)
    
    # Display the circuit
    print("Quantum Phase Estimation Circuit:")
    print(qc.draw())
    print()
    
    # Simulate the circuit
    simulator = AerSimulator()
    job = simulator.run(qc, shots=1024)
    result = job.result()
    counts = result.get_counts(qc)
    
    print("Measurement counts:")
    print(counts)
    print()
    
    # Process the result: find the most frequent outcome
    outcome = max(counts, key=counts.get)
    decimal = int(outcome, 2)
    estimated_phase = decimal / (2 ** num_counting_qubits)
    
    print(f"Most frequent outcome: {outcome} (binary)")
    print(f"Decimal value: {decimal}")
    print(f"Estimated phase (θ/2π): {estimated_phase * (2 * np.pi):.6f} rad")
    print(f"Estimated phase (θ/2π): {estimated_phase:.6f}")
    print(f"Expected phase (θ/2π): 0.375000")
    print(f"Absolute error: {abs(estimated_phase - 0.375):.6f}")
    
    # Plot histogram
    try:
        plot_histogram(counts)
        plt.title(f"QPE Results (θ/2π = 0.375)")
        plt.show()
    except:
        # If plotting fails, just print the results
        print("Plotting not available in this environment")
    
    return estimated_phase

if __name__ == "__main__":
    print("Running Quantum Phase Estimation Example")
    print("=" * 50)
    estimated_phase = run_qpe_example()
    print("\n" + "=" * 50)
    print("Example completed successfully!")