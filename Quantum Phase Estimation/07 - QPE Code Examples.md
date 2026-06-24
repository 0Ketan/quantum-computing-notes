# 07 — QPE Code Examples (Qiskit)

> *"The best way to learn QPE is to code it yourself. Run these examples, modify them, and experiment."*

---

## 📦 Setup

Make sure you have Qiskit installed:

```bash
pip install qiskit qiskit-aer matplotlib numpy pylatexenc
```

---

## 1️⃣ Building Blocks: Phase Kickback Demonstration

Before QPE, let's verify phase kickback works:

```python
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import numpy as np

def phase_kickback_demo(theta=0.25):
    """
    Demonstrate phase kickback with 1 control qubit.
    U|ψ⟩ = e^{2πi·θ}|ψ⟩, here U = P(2π·θ) (phase gate)
    """
    # Phase gate P(φ) = |0⟩⟨0| + e^{iφ}|1⟩⟨1|
    
    qc = QuantumCircuit(2, 1)  # 2 qubits, 1 classical bit
    
    # Initialize target qubit to |1⟩ (eigenstate of P gate)
    qc.x(1)
    
    # Apply Hadamard to control
    qc.h(0)
    
    # Controlled-Phase gate (phase kickback)
    # CP(φ) applies phase φ to |11⟩ state
    qc.cp(2 * np.pi * theta, 0, 1)
    
    # Hadamard on control again
    qc.h(0)
    
    # Measure control qubit
    qc.measure(0, 0)
    
    return qc

# Test with θ = 0.0, 0.25, 0.5, 0.75
for theta in [0.0, 0.25, 0.5, 0.75]:
    qc = phase_kickback_demo(theta)
    
    # Simulate
    sim = AerSimulator()
    t_qc = transpile(qc, sim)
    result = sim.run(t_qc, shots=1024).result()
    counts = result.get_counts()
    
    # The probability of |0⟩ should be cos²(π·θ)
    prob_0 = np.cos(np.pi * theta)**2
    print(f"θ = {theta:.2f}: P(0) predicted = {prob_0:.3f}, measured = {counts.get('0', 0)/1024:.3f}")
```

**Expected Output:**
```
θ = 0.00: P(0) predicted = 1.000, measured = 1.000
θ = 0.25: P(0) predicted = 0.500, measured = 0.498
θ = 0.50: P(0) predicted = 0.000, measured = 0.000
θ = 0.75: P(0) predicted = 0.500, measured = 0.502
```

### Circuit Visualization

The phase kickback circuit for $\theta = 0.25$:

![[Diagrams/01_phase_kickback.png]]

```
     ┌───┐         ┌───┐┌─┐
q_0: ┤ H ├──■──────┤ H ├┤M├
     └───┘│π/2    └───┘└╥┘
q_1: ─────■──────────────╫─
          │              ║
c: 1/═════╧══════════════╩═
```

---

## 2️⃣ Implementing the Quantum Fourier Transform (QFT)

QPE needs the IQFT (Inverse QFT). Let's build both:

![[Diagrams/02_qft_3qubit.png]]

![[Diagrams/03_iqft_3qubit.png]]

```python
from qiskit import QuantumCircuit
import numpy as np

def qft(n):
    """Create a Quantum Fourier Transform circuit on n qubits."""
    qc = QuantumCircuit(n, name="QFT")
    
    # Apply Hadamard + controlled rotations qubit by qubit
    for qubit in range(n - 1, -1, -1):
        qc.h(qubit)
        for target in range(qubit - 1, -1, -1):
            angle = np.pi / (2 ** (qubit - target))
            qc.cp(angle, target, qubit)
    
    # Swap qubits to reverse order
    for i in range(n // 2):
        qc.swap(i, n - i - 1)
    
    return qc

def iqft(n):
    """Create an Inverse Quantum Fourier Transform circuit on n qubits."""
    qc = QuantumCircuit(n, name="IQFT")
    
    # Reverse QFT operations
    for i in range(n // 2):
        qc.swap(i, n - i - 1)
    
    for qubit in range(n):
        for target in range(qubit):
            angle = -np.pi / (2 ** (qubit - target))  # Negative angle = inverse
            qc.cp(angle, target, qubit)
        qc.h(qubit)
    
    return qc

# Test: QFT† · QFT = Identity
n = 4
qft_circ = qft(n)
iqft_circ = iqft(n)

full_circ = qft_circ.compose(iqft_circ)
print("QFT + IQFT circuit depth:", full_circ.depth())
print("Both circuits should combine to identity (QFT† · QFT = I)")
```

### Visualizing QFT on |000⟩:

```python
# Demonstrate QFT on |000⟩
n = 3
qc = QuantumCircuit(n)

# QFT on |000⟩ should give equal superposition
qc.append(qft(n), range(n))

# Measure to verify
qc.measure_all()

# Simulate
sim = AerSimulator()
t_qc = transpile(qc, sim)
result = sim.run(t_qc, shots=4096).result()
counts = result.get_counts()
print("QFT on |000⟩:", counts)
# Should be roughly uniform distribution over all 8 basis states
```

---

## 3️⃣ Full QPE Implementation

Now let's implement the complete QPE algorithm:

```python
from qiskit import QuantumCircuit, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import numpy as np

def qpe_circuit(U, n_control, target_qubits, theta):
    """
    Generic QPE circuit generator.
    
    Args:
        U: Unitary gate (as a Qiskit Gate)
        n_control: Number of control qubits
        target_qubits: List of qubit indices for target register
        theta: Expected phase (for setting up the eigenstate)
    
    Returns:
        QuantumCircuit: The complete QPE circuit (without measurement)
        int: The expected outcome (2^n * theta)
    """
    n_total = n_control + len(target_qubits)
    qc = QuantumCircuit(n_total, n_control)
    
    # Step 1: Initialize target to eigenstate of U
    # For the phase gate P(φ), the eigenstate with eigenvalue e^{iφ} is |1⟩
    qc.x(target_qubits[0])
    
    # Step 2: Apply Hadamard to all control qubits
    for qubit in range(n_control):
        qc.h(qubit)
    
    # Step 3: Apply controlled-U^{2^k} operations
    for k in range(n_control):
        # Apply U^{2^k} controlled by control qubit k
        # For phase gate: U^{2^k} = P(2π·θ·2^k)
        angle = 2 * np.pi * theta * (2 ** k)
        qc.cp(angle, k, target_qubits[0])
    
    # Step 4: Apply Inverse QFT
    iqft_gate = iqft(n_control).to_gate()
    qc.append(iqft_gate, range(n_control))
    
    # Step 5: Measure
    for qubit in range(n_control):
        qc.measure(qubit, qubit)
    
    expected = int(2**n_control * theta) % (2**n_control)
    return qc, expected
```

### Example 1: Perfect Phase (Exactly Representable)

```python
# θ = 0.5 (perfect: 0.5 = 1/2, exactly representable with 1 bit)
n_control = 3
theta = 0.5

qc, expected = qpe_circuit(None, n_control, [n_control], theta)

sim = AerSimulator()
t_qc = transpile(qc, sim)
result = sim.run(t_qc, shots=4096).result()
counts = result.get_counts()

# Expected outcome: 2^3 * 0.5 = 4 = binary '100'
print(f"θ = {theta}")
print(f"Expected: {expected} = {bin(expected)[2:].zfill(n_control)}")
print(f"Measured: {counts}")
print(f"Correct %: {counts.get(format(expected, f'0{n_control}b'), 0)/4096*100:.1f}%")
```

**Expected Output:**
```
θ = 0.5
Expected: 4 = 100
Measured: {'100': 4096}
Correct %: 100.0%
```

### Example 2: Arbitrary Phase

```python
# θ = 0.375 = 3/8, exactly representable with 3 bits
theta = 0.375
qc, expected = qpe_circuit(None, 4, [4], theta)

sim = AerSimulator()
t_qc = transpile(qc, sim)
result = sim.run(t_qc, shots=4096).result()
counts = result.get_counts()

print(f"θ = {theta}")
print(f"Expected: {expected} = {bin(expected)[2:].zfill(4)}")
print(f"Measured: {counts}")

# Extract phase estimate
measured_val = int(max(counts, key=counts.get), 2)
theta_est = measured_val / (2**4)
print(f"Estimated θ = {theta_est}")
print(f"True θ = {theta}")
print(f"Error = {abs(theta_est - theta)}")
```

### Example 3: Non-Exact Phase

The QPE circuit for this example:

![[Diagrams/06_shor_period_finding.png]]

```python
# θ = 1/3 ≈ 0.3333... (not exactly representable)
theta = 1/3
n_control = 5

qc, expected = qpe_circuit(None, n_control, [n_control], theta)

sim = AerSimulator()
t_qc = transpile(qc, sim)
result = sim.run(t_qc, shots=8192).result()
counts = result.get_counts()

# Best estimate
measured_val = int(max(counts, key=counts.get), 2)
theta_est = measured_val / (2**n_control)

print(f"True θ = {theta}")
print(f"2^{n_control}·θ = {2**n_control * theta}")
print(f"Best estimate: {measured_val}/{2**n_control} = {theta_est}")
print(f"Error: {abs(theta_est - theta)}")

# Show distribution
print(f"\nTop outcomes:")
for outcome, count in sorted(counts.items(), key=lambda x: -x[1])[:5]:
    val = int(outcome, 2) / (2**n_control)
    print(f"  {outcome} → θ ≈ {val:.4f} ({count} shots, {count/8192*100:.1f}%)")
```

---

## 4️⃣ QPE with a Custom Unitary Matrix

Let's use QPE to find the eigenvalue of a real unitary matrix:

```python
from qiskit.quantum_info import Operator
import numpy as np

# Create a unitary matrix with known eigenvalues
# Let's use: U = [[1, 0], [0, e^{2πiθ}]]
theta = 0.25
U_matrix = np.array([[1, 0], 
                     [0, np.exp(2j * np.pi * theta)]])
U_op = Operator(U_matrix)

# The eigenstate with eigenvalue e^{2πiθ} is |1⟩
# So we prepare |1⟩ on the target register

n_control = 4
qc = QuantumCircuit(n_control + 1, n_control)

# Initialize target to eigenstate
qc.x(n_control)  # |1⟩

# Hadamards on control
for q in range(n_control):
    qc.h(q)

# Controlled-unitary operations
# U^{2^k} has eigenvalues {1, e^{2πiθ·2^k}}
for k in range(n_control):
    # Controlled-U^{2^k}
    angle = 2 * np.pi * theta * (2**k)
    qc.cp(angle, k, n_control)

# IQFT
iqft_gate = iqft(n_control).to_gate()
qc.append(iqft_gate, range(n_control))

# Measure
for q in range(n_control):
    qc.measure(q, q)

# Simulate
sim = AerSimulator()
t_qc = transpile(qc, sim)
result = sim.run(t_qc, shots=4096).result()
counts = result.get_counts()

print(f"QPE on U with θ = {theta}")
measured_val = int(max(counts, key=counts.get), 2)
theta_est = measured_val / (2**n_control)
print(f"Estimated θ = {theta_est}")
print(f"Exact θ = {theta}")
```

---

## 5️⃣ IQPE: Iterative Quantum Phase Estimation

This version uses only 1 control qubit:

![[Diagrams/07_iqpe_single_iteration.png]]

and is much more NISQ-friendly:

```python
def iqpe_single_bit(U_gate, n_qubits_estimate, n_shots=1024):
    """
    Iterative Quantum Phase Estimation using 1 control qubit.
    
    This adaptively estimates θ bit by bit, from most significant to least.
    """
    theta_estimate = 0.0
    
    for k in range(n_qubits_estimate - 1, -1, -1):
        # Prepare circuit for bit k
        qc = QuantumCircuit(2, 1)  # 1 control + 1 target, 1 classical
        
        # Initialize target to eigenstate |1⟩
        qc.x(1)
        
        # Hadamard on control
        qc.h(0)
        
        # Apply controlled-U^{2^k}
        qc.cp(2 * np.pi * (2**k), 0, 1)
        
        # Apply phase correction based on previously measured bits
        # This rotates out the contribution from higher-order bits
        phase_correction = 0.0
        for j in range(k + 1, n_qubits_estimate):
            bit_val = (theta_estimate * (2**n_qubits_estimate) // (2**j)) % 2
            phase_correction += 2 * np.pi * bit_val / (2**(j - k))
        
        if phase_correction > 0:
            qc.p(-phase_correction, 0)
        
        # Hadamard on control
        qc.h(0)
        
        # Measure
        qc.measure(0, 0)
        
        # Simulate
        sim = AerSimulator()
        t_qc = transpile(qc, sim)
        result = sim.run(t_qc, shots=n_shots).result()
        counts = result.get_counts()
        
        # Determine bit k
        bit = 0 if counts.get('0', 0) > counts.get('1', 0) else 1
        theta_estimate += bit / (2**(n_qubits_estimate - k))
        
        print(f"Bit {k}: measured '{bit}' → θ so far = {theta_estimate:.6f}")
    
    return theta_estimate

# Test IQPE
true_theta = 0.375  # 3/8
print(f"True θ = {true_theta}")
print(f"IQPE estimation:\n" + "="*40)

estimated = iqpe_single_bit(None, 8)
print(f"\nFinal estimate: θ ≈ {estimated:.6f}")
print(f"True value:     θ = {true_theta:.6f}")
print(f"Error:          {abs(estimated - true_theta):.2e}")
```

---

## 6️⃣ QPE for Quantum Chemistry: H₂ Molecule

This is a simplified example showing how QPE finds the energy of H₂:

```python
from qiskit.quantum_info import SparsePauliOp
from scipy.linalg import expm
import numpy as np

# H₂ Hamiltonian in STO-3G basis (simplified)
# H = g0 I + g1 ZZ + g2 XX + g3 YY (with Z_0 Z_1, X_0 X_1, Y_0 Y_1)
h2_hamiltonian = SparsePauliOp([
    'II', 'ZZ', 'XX', 'YY'
], coeffs=[
    -1.052373245772859,
    0.39793742484318045,
    0.39793742484318045,
    0.18093119978423156
])

def h2_qpe_simulation(bond_length=0.735):  # Angstroms
    """
    Simplified QPE for H₂ molecule ground state energy.
    
    In practice, we'd need:
    1. Full electronic structure Hamiltonian
    2. Jordan-Wigner or Bravyi-Kitaev mapping
    3. Trotter decomposition for e^{-iHt}
    4. State preparation (HF state)
    
    Here we use the known ground state energy for demonstration.
    """
    # The ground state energy of H₂ at equilibrium bond length
    E0 = -1.857  # Hartree (approximate)
    
    print(f"H₂ molecule at bond length {bond_length} Å")
    print(f"Expected ground state energy: {E0:.3f} Hartree")
    print(f"Expected ground state energy: {E0 * 27.2114:.2f} eV")
    
    # For a full QPE implementation:
    # 1. Map H₂ Hamiltonian to 2 qubits (Bravyi-Kitaev or Jordan-Wigner)
    # 2. Prepare Hartree-Fock state |01⟩
    # 3. Apply controlled-e^{-iHt} using Trotter decomposition
    # 4. Run QPE on 4-8 control qubits for chemical accuracy
    # 5. Measure and extract energy
    # 6. Repeat with error mitigation
    
    print("\n🏗️ Full implementation requires:")
    print("  - Qiskit Nature (for molecular Hamiltonians)")
    print("  - Trotterization of time evolution")
    print("  - Initial state preparation (HF)")
    print("  - Control register of 8+ qubits for chemical accuracy")
    
    return E0

E0 = h2_qpe_simulation()
```

---

## 7️⃣ Visualizing QPE Results

```python
import matplotlib.pyplot as plt

def plot_qpe_results(counts, n_control, true_theta=None):
    """Visualize QPE measurement outcomes."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Convert binary outcomes to decimal
    outcomes = {}
    for bitstring, count in counts.items():
        val = int(bitstring, 2)
        theta = val / (2**n_control)
        outcomes[theta] = count
    
    # Bar chart
    thetas = sorted(outcomes.keys())
    probs = [outcomes[t] / sum(outcomes.values()) for t in thetas]
    
    ax1.bar(thetas, probs, width=1/(2**n_control), 
            color='royalblue', edgecolor='navy', alpha=0.7)
    ax1.set_xlabel('Estimated θ')
    ax1.set_ylabel('Probability')
    ax1.set_title('QPE Measurement Distribution')
    
    # Highlight true value
    if true_theta is not None:
        ax1.axvline(x=true_theta, color='red', linestyle='--', 
                   linewidth=2, label=f'True θ = {true_theta}')
        ax1.legend()
    
    # Cumulative histogram
    ax2.bar(thetas, np.cumsum(probs), width=1/(2**n_control),
            color='seagreen', alpha=0.7)
    ax2.set_xlabel('Estimated θ')
    ax2.set_ylabel('Cumulative Probability')
    ax2.set_title('Cumulative Distribution')
    
    if true_theta is not None:
        ax2.axvline(x=true_theta, color='red', linestyle='--', 
                   linewidth=2, label=f'True θ = {true_theta}')
        ax2.legend()
    
    plt.tight_layout()
    plt.savefig('qpe_results.png', dpi=150)
    plt.close()
    print("Saved: qpe_results.png")

# Example usage
# plot_qpe_results(counts, n_control=5, true_theta=1/3)
```

---

## 🧪 Exercises for You

### Exercise 1: Noise in QPE
Modify the QPE circuit to add noise channels and observe the degradation:

```python
from qiskit.providers.aer.noise import NoiseModel, depolarizing_error

def add_noise(qc, p_depolarizing=0.001):
    """Add depolarizing noise to a circuit."""
    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(
        depolarizing_error(p_depolarizing, 1), ['h', 'p'])
    noise_model.add_all_qubit_quantum_error(
        depolarizing_error(p_depolarizing * 5, 2), ['cp'])
    return noise_model
```

**Try:** Run QPE with $p = 0.001, 0.01, 0.1$ and see how accuracy degrades.

### Exercise 2: More Control Qubits
Run QPE for $\theta = 1/\pi$ with $n = 6, 8, 10$ control qubits. How does precision scale?

### Exercise 3: Different Eigenstates
What happens if your initial state is NOT an eigenstate of $U$? Try preparing $|+\rangle$ instead of $|1\rangle$.

### Exercise 4: Implement Shor's Period Finding
Build the modular exponentiation unitary $U|y\rangle = |ay \mod N\rangle$ for small $N$ (like $N=15$).

### Exercise 5: Trotter Error
For the chemistry example, implement Trotter decomposition $e^{-iHt} \approx (e^{-iH\Delta t})^r$ and study how the Trotter step size affects the energy estimate.

---

## 📊 Code Summary

| Snippet | What It Teaches |
|---------|-----------------|
| Phase kickback demo | Core mechanism of QPE |
| QFT/IQFT implementation | The Fourier transform on qubits |
| Full QPE circuit | Complete algorithm |
| Non-exact phase | Error behavior |
| IQPE (iterative) | NISQ-friendly variant |
| Chemistry example | Real-world mapping |
| Noise simulation | Hardware reality |

---

## 🎯 Check Your Understanding

1. ❓ **Run the QPE code for $\theta = 0.3$ with $n=5$ bits. What's the probability of getting the exact answer?**
2. ❓ **Modify the code to use 8 control qubits for $\theta = 1/3$. How does accuracy improve?**
3. ❓ **Implement the IQPE and compare the circuit depth with standard QPE.**
4. ❓ **Add measurement errors to the simulation. At what error rate does QPE break?**

---

[[06 - Advantages Challenges Future|← Previous: Advantages & Challenges]] | [[00 - QPE Study Guide Home|Study Guide]] | [[08 - Practice Problems|Next: Practice Problems →]]
