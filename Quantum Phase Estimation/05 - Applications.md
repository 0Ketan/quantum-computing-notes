# 05 — Applications of Quantum Phase Estimation

> *"QPE is the engine under the hood of the most powerful quantum algorithms."*

---

## 1️⃣ Shor's Algorithm: Breaking RSA Encryption

### The Problem

**RSA encryption** relies on the fact that factoring large numbers is classically hard:

> Given $N = p \times q$ (where $p,q$ are large primes), find $p$ and $q$.

The best classical algorithm (General Number Field Sieve) takes **exponential time**. Shor's algorithm does it in **polynomial time** — and QPE is the key subroutine.

### How Shor Uses QPE

#### Step 1: Reduce Factoring to Order Finding

Factor $N$ by finding the **order** of a random $a$ modulo $N$:
- Pick $a$ where $1 < a < N$ and $\gcd(a,N) = 1$
- Find the smallest $r > 0$ such that $a^r \equiv 1 \ (\text{mod} \ N)$
- $r$ is called the **order** of $a$ modulo $N$
- If $r$ is even, compute $\gcd(a^{r/2} \pm 1, N)$ — this gives factors!

#### Step 2: Set Up QPE for Order Finding

Define the unitary operator $U$:

$$U|y\rangle = |ay \ \text{mod} \ N\rangle$$

This is a **modular multiplication** operator. Its eigenstates are:

$$|u_s\rangle = \frac{1}{\sqrt{r}}\sum_{k=0}^{r-1} e^{-2\pi i s k/r} |a^k \ \text{mod} \ N\rangle$$

with eigenvalues:

$$U|u_s\rangle = e^{2\pi i s/r}|u_s\rangle$$

So the phase $\theta = s/r$!

#### Step 3: QPE Extracts $s/r$

- Run QPE with $U$ as the modular multiplication operator
- The measured phase gives $\tilde{\theta} = s/r$
- Use continued fractions to extract $r$ from $\tilde{\theta}$

#### Step 4: Factor $N$

Once we have $r$:
1. If $r$ is odd, try a different $a$
2. Compute $p = \gcd(a^{r/2} + 1, N)$ and $q = \gcd(a^{r/2} - 1, N)$
3. $N = p \times q$ — factoring complete!

### 📊 Complexity Comparison

| Algorithm | Time Complexity | Year |
|-----------|----------------|------|
| Trial division | $O(e^{n/2})$ | Ancient |
| General Number Field Sieve | $O(e^{(\log N)^{1/3} (\log \log N)^{2/3}})$ | 1990s |
| **Shor's Algorithm (QPE)** | **$O((\log N)^3)$** | **1994** |

> **💡 Key Insight:** Shor's algorithm is **exponentially faster** than the best classical algorithm for factoring. This is why large-scale quantum computers would break RSA encryption.

---

## 2️⃣ Quantum Chemistry: Finding Molecular Energies

### The Problem

Quantum chemists want to find the **ground state energy** of molecules:

$$H|\psi_0\rangle = E_0|\psi_0\rangle$$

where $H$ is the molecular Hamiltonian and $E_0$ is the ground state energy.

Classically, this scales **exponentially** with the number of electrons — even a modest molecule like caffeine is intractable for classical computers.

### How QPE Solves This

#### Step 1: Map the Problem to Qubits

The molecular Hamiltonian $H$ is mapped to a **qubit Hamiltonian**:

$$H = \sum_i h_i P_i$$

where $P_i$ are Pauli strings (tensor products of $I, X, Y, Z$).

#### Step 2: Create a Unitary from the Hamiltonian

Define:

$$U = e^{-iHt/\hbar}$$

This is the **time evolution operator**. Its eigenvalues are $e^{-iE_k t/\hbar}$.

#### Step 3: Prepare an Initial State

Use classical methods (HF, CISD) to prepare $|\psi_{\text{init}}\rangle$ that has **good overlap** with the true ground state $|\psi_0\rangle$.

#### Step 4: Run QPE

- Apply QPE with $U = e^{-iHt}$
- The measured phase reveals $E_0$ (the ground state energy)
- Repeat and take statistics to suppress errors

### 🔬 Real-World Impact

QPE-based quantum chemistry could revolutionize:

| Field | Application |
|-------|-------------|
| **Drug Discovery** | Simulating protein-ligand binding |
| **Catalysis** | Designing better catalysts (e.g., nitrogen fixation) |
| **Materials** | Finding novel superconductors |
| **Energy** | Designing battery materials (see Section 3) |

### Example: Hydrogen Molecule (H₂)

![[Diagrams/12_h2_groundstate_qpe.png]]

The Hamiltonian for H₂ in the STO-3G basis:

$$H = h_0 I + h_1 Z_0 + h_2 Z_1 + h_3 Z_0 Z_1 + h_4 X_0 X_1 + h_5 Y_0 Y_1$$

Preparing $|\psi_{\text{init}}\rangle = |01\rangle$ and running QPE reveals:

$$E_0 \approx -1.137 \ \text{Hartree}$$

(A Hartree ≈ 27.2 eV, the atomic unit of energy)

---

## 3️⃣ Materials Science: Fuel Cells, Flow Batteries, and Energy Storage

### The Challenge

Modern energy storage (lithium-ion batteries, fuel cells, flow batteries) relies on understanding **quantum-level interactions**:

```
  ┌─────────────────────────────────────────────────┐
  │           ENERGY STORAGE MATERIALS              │
  ├──────────────────┬──────────────────┬────────────┤
  │  Li-ion Battery  │   Fuel Cell      │ Flow       │
  │  Materials       │   Catalysts      │ Battery    │
  │                  │                  │ Materials  │
  ├──────────────────┼──────────────────┼────────────┤
  │ LiCoO₂          │ Pt nanoparticles │ V²⁺/V³⁺     │
  │ LiFePO₄         │ Ni-based MOFs    │ Zn/Br₂     │
  │ Si anodes       │ Perovskites      │ Fe/Cr      │
  │ Solid electrolytes│                 │            │
  └──────────────────┴──────────────────┴────────────┘
```

### How QPE Helps

#### Finding Redox Potentials

In flow batteries, the **redox potential** determines the voltage:

$$E_{\text{cell}} = E_{\text{cathode}} - E_{\text{anode}}$$

QPE can compute these energies to chemical accuracy ($\pm 1$ kcal/mol ≈ $\pm 0.043$ eV).

#### Simulating Catalytic Reactions

For fuel cells, the oxygen reduction reaction:

$$O_2 + 4H^+ + 4e^- \rightarrow 2H_2O$$

requires understanding transition states — QPE can compute these energies.

#### Band Gap Engineering

For solar cell materials and battery electrodes, the **band gap** determines conductivity:

$$E_{\text{gap}} = E_{\text{LUMO}} - E_{\text{HOMO}}$$

QPE can compute both energies and thus the band gap.

### 📈 Impact Metrics

| Application | Current Best Classical | QPE-Enhanced Potential |
|-------------|----------------------|----------------------|
| Battery capacity | ~300 Wh/kg | **>500 Wh/kg** |
| Fuel cell efficiency | ~60% | **>80%** |
| Catalyst discovery | Trial & error (~10 yrs) | **Computational screening (~1 yr)** |

---

## 4️⃣ HHL Algorithm: Solving Linear Systems

### The Problem

Solve $A\vec{x} = \vec{b}$ where $A$ is an $N \times N$ matrix.

Classically this takes $O(N \log N)$ (with Gaussian elimination) to $O(N^3)$.

### How HHL Uses QPE

HHL encodes $\vec{b}$ as a quantum state $|b\rangle$ and uses QPE to find eigenvalues of $e^{iAt}$:

1. **QPE** extracts eigenvalues $\lambda_j$ of $A$
2. **Phase rotation** inverts eigenvalues $\lambda_j \rightarrow \lambda_j^{-1}$
3. **IQFT + measurement** yields $|x\rangle \propto A^{-1}|b\rangle$

**Complexity:** $O((\log N)^2 \kappa^2 / \epsilon)$ where $\kappa$ is the condition number and $\epsilon$ is precision.

---

## 5️⃣ Additional Applications

### Quantum Principal Component Analysis (PCA)

- Use QPE to find eigenvalues of covariance matrices
- Exponential speedup for dimensionality reduction

### Quantum Metrology

- Use QPE for **super-resolution** sensing
- Beat the standard quantum limit in measurements
- Applications: atomic clocks, gravitational wave detection, MRI

### Quantum Signal Processing

- Extract frequencies from quantum signals
- Quantum version of the classical Fourier transform
- Applications: spectroscopy, communications

---

## 📊 Applications Summary Table

![[Diagrams/11_qpe_applications_map.png]]

| Algorithm/Application | What QPE Does | Speedup |
|----------------------|---------------|---------|
| **Shor's Algorithm** | Order finding for factoring | Exponential |
| **Quantum Chemistry** | Ground state energy | Exponential |
| **Materials Science** | Band gaps, redox potentials | Exponential |
| **HHL Algorithm** | Matrix eigenvalues | Exponential |
| **Quantum PCA** | Covariance eigenvalues | Exponential |
| **Quantum Metrology** | Parameter estimation | Quadratic |
| **Signal Processing** | Frequency extraction | Exponential |

---

## 🎯 Check Your Understanding

1. ❓ **Explain how Shor's algorithm reduces factoring to order finding.**
2. ❓ **Why is QPE well-suited for quantum chemistry problems?**
3. ❓ **What is "chemical accuracy" and why does it matter for battery research?**
4. ❓ **How does the HHL algorithm use QPE to solve linear systems?**
5. ❓ **Which application do you think will have the biggest real-world impact first? Why?**

---

[[04 - Mathematical Derivations|← Previous: Math Derivations]] | [[00 - QPE Study Guide Home|Study Guide]] | [[06 - Advantages Challenges Future|Next: Advantages & Challenges →]]
