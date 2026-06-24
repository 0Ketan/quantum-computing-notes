# 03 — Working Principle of QPE

> *"The QPE algorithm is a beautiful marriage of phase kickback and the quantum Fourier transform."*

---

## 🏗️ The QPE Circuit: High-Level View

![[Diagrams/04_qpe_full_4qubit.png]]

![[Diagrams/05_qpe_3ctrl_compact.png]]

> **Control register** (n qubits, top) → Holds the estimated phase  
> **Target register** (m qubits, bottom) → Eigenstate of $U$

---

## 🔬 Step-by-Step Walkthrough

### Step 0: Setup

We have:
- A unitary operator $U$ acting on $m$ qubits
- An eigenstate $|\psi\rangle$ of $U$: $U|\psi\rangle = e^{2\pi i\theta}|\psi\rangle$
- $n$ control qubits initialized to $|0\rangle$

**Initial state:**

$$|\Psi_0\rangle = |0\rangle^{\otimes n} \otimes |\psi\rangle$$

### Step 1: Apply Hadamard Gates to All Control Qubits

Apply $H^{\otimes n}$ to the control register:

$$|\Psi_1\rangle = (H^{\otimes n}|0\rangle^{\otimes n}) \otimes |\psi\rangle = \frac{1}{\sqrt{2^n}}\sum_{j=0}^{2^n-1} |j\rangle \otimes |\psi\rangle$$

**What happened:** The control register is now in a **uniform superposition** of all $2^n$ basis states. Each basis state $|j\rangle$ will "probe" the phase differently.

> **📝 Detailed expansion:**
> $$H^{\otimes n}|0\rangle^{\otimes n} = \frac{1}{\sqrt{2^n}} \sum_{x \in \{0,1\}^n} |x\rangle = \frac{1}{\sqrt{2^n}}(|0\rangle + |1\rangle) \otimes (|0\rangle + |1\rangle) \otimes \cdots \otimes (|0\rangle + |1\rangle)$$

### Step 2: Apply Controlled-Unitary Operations

This is the **phase encoding** step. For each control qubit $k$ (indexed from 0, the bottom of the control register, to $n-1$, the top), we apply controlled-$U^{2^k}$:

$$|\Psi_2\rangle = \frac{1}{\sqrt{2^n}}\sum_{j=0}^{2^n-1} |j\rangle \otimes U^j|\psi\rangle$$

Since $|\psi\rangle$ is an eigenstate of $U$:

$$U^j|\psi\rangle = (e^{2\pi i\theta})^j |\psi\rangle = e^{2\pi i\theta j}|\psi\rangle$$

Therefore:

$$|\Psi_2\rangle = \frac{1}{\sqrt{2^n}}\sum_{j=0}^{2^n-1} e^{2\pi i\theta j} |j\rangle \otimes |\psi\rangle$$

**Now the phase is encoded in the control register!** The control qubits are in a superposition where each basis state $|j\rangle$ has picked up a phase proportional to $\theta \times j$.

> **💡 Intuition:** Think of each controlled-$U^{2^k}$ as "writing one bit" of the phase onto the control qubits. The bottom control qubit applies $U^1$, the next applies $U^2$, then $U^4$, $U^8$, etc.

### Step 3: Apply Inverse Quantum Fourier Transform (IQFT)

The state of the control register is:

$$\frac{1}{\sqrt{2^n}}\sum_{j=0}^{2^n-1} e^{2\pi i\theta j} |j\rangle$$

This is exactly the **quantum Fourier transform** of the state $|2^n\theta\rangle$!

The IQFT "undoes" the Fourier transform, converting the phase-encoded state into a basis state that reveals $\theta$:

$$|\Psi_3\rangle = \text{QFT}^\dagger \left(\frac{1}{\sqrt{2^n}}\sum_{j=0}^{2^n-1} e^{2\pi i\theta j} |j\rangle\right) \otimes |\psi\rangle$$

**For the ideal case where $\theta = \frac{\phi}{2^n}$ (exactly representable):**
$$|\Psi_3\rangle = |\phi\rangle \otimes |\psi\rangle$$

Where $\phi = 2^n\theta$ is the integer representation of the phase.

**For the general case where $\theta$ is not exactly representable:**
$$|\Psi_3\rangle \approx \sum_{k} c_k |k\rangle \otimes |\psi\rangle$$
with high probability concentrated near $k = \lfloor 2^n\theta \rceil$.

### Step 4: Measure the Control Register

Measure all $n$ control qubits. The measurement result $\tilde{\phi}$ gives us:

$$\tilde{\theta} = \frac{\tilde{\phi}}{2^n}$$

which is our estimate of $\theta$.

**Accuracy:** The estimate is accurate to $n$ bits with probability at least $\frac{4}{\pi^2} \approx 0.405$. By adding $n + \lceil \log_2(2 + \frac{1}{2\epsilon})\rceil$ qubits, we can succeed with probability $1-\epsilon$.

---

## 🧪 Detailed Quantum State Evolution

Let's trace through a concrete example with $n=3$ control qubits and $\theta = 0.375 = \frac{3}{8}$.

### Initial State
$$|\Psi_0\rangle = |000\rangle \otimes |\psi\rangle$$

### After Hadamards
$$|\Psi_1\rangle = \frac{1}{\sqrt{8}}(|000\rangle + |001\rangle + |010\rangle + |011\rangle + |100\rangle + |101\rangle + |110\rangle + |111\rangle) \otimes |\psi\rangle$$

### After Controlled-Unitaries
For each basis state $|j\rangle$, the phase $e^{2\pi i \theta j}$ is applied:

| $j$ (binary) | $j$ (decimal) | Phase $e^{2\\pi i(0.375)j}$ | 
|-------------|---------------|---------------------------|
| 000 | 0 | $e^0 = 1$ |
| 001 | 1 | $e^{2\\pi i(0.375)} = e^{i3\\pi/4}$ |
| 010 | 2 | $e^{2\\pi i(0.75)} = e^{i3\\pi/2}$ |
| 011 | 3 | $e^{2\\pi i(1.125)} = e^{i\\pi/4}$ |
| 100 | 4 | $e^{2\\pi i(1.5)} = e^{i\\pi}$ |
| 101 | 5 | $e^{2\\pi i(1.875)} = e^{i7\\pi/4}$ |
| 110 | 6 | $e^{2\\pi i(2.25)} = e^{i\\pi/2}$ |
| 111 | 7 | $e^{2\\pi i(2.625)} = e^{i5\\pi/4}$ |

$$|\Psi_2\rangle = \frac{1}{\sqrt{8}}\left(|000\rangle + e^{i3\pi/4}|001\rangle + e^{i3\pi/2}|010\rangle + e^{i\pi/4}|011\rangle + e^{i\pi}|100\rangle + e^{i7\pi/4}|101\rangle + e^{i\pi/2}|110\rangle + e^{i5\pi/4}|111\rangle\right) \otimes |\psi\rangle$$

### After IQFT → Measurement

The IQFT transforms this to approximately $|011\rangle = |3\rangle$ (since $2^n\theta = 8 \times 0.375 = 3$).

$$\tilde{\theta} = \frac{3}{8} = 0.375 \quad \text{✅ Correct!}$$

---

## 🔄 Phase Kickback in Detail

The heart of QPE is **phase kickback**. Let's understand it deeply.

### Simple Case: Single Control Qubit

![[Diagrams/01b_phase_kickback_circuit.png]]

```
|0⟩ ──H──•── H ── M
         │
|ψ⟩ ────U───────
```

where $U|\psi\rangle = e^{2\pi i\theta}|\psi\rangle$.

**Step 1:** $H|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$

**Step 2:** $\text{C-}U \left(\frac{|0\rangle + |1\rangle}{\sqrt{2}} \otimes |\psi\rangle\right) = \frac{|0\rangle \otimes |\psi\rangle + |1\rangle \otimes U|\psi\rangle}{\sqrt{2}}$
$$= \frac{|0\rangle \otimes |\psi\rangle + |1\rangle \otimes e^{2\pi i\theta}|\psi\rangle}{\sqrt{2}}$$
$$= \frac{|0\rangle + e^{2\pi i\theta}|1\rangle}{\sqrt{2}} \otimes |\psi\rangle$$

**The phase "kicked back"** from the target to the control qubit!

### Why Does This Work?

The key is that $|\psi\rangle$ is an eigenstate. When $U$ is applied, the change is just a global phase on the target register — but relative to the control register, it becomes a **relative phase**:

$$
\frac{|0\rangle + |1\rangle}{\sqrt{2}} \otimes |\psi\rangle \xrightarrow{\text{C-}U} \frac{|0\rangle + e^{2\pi i\theta}|1\rangle}{\sqrt{2}} \otimes |\psi\rangle
$$

### The Phase as Rotation on the Bloch Sphere

The state $\frac{|0\rangle + e^{2\pi i\theta}|1\rangle}{\sqrt{2}}$ looks like this on the Bloch sphere:

```
For θ = 0:     For θ = 0.25:   For θ = 0.5:    For θ = 0.75:
   |0⟩             |0⟩             |0⟩             |0⟩
    ▲               ▲               ▲               ▲
    |               |               |               |
───●───→        ───●──→         ●───→         ●───→──
    |           ↗  |           |               |  ↖
    ▼               ▼               ▼               ▼
   |1⟩             |1⟩             |1⟩             |1⟩
   θ=0            θ=0.25         θ=0.5           θ=0.75
```

The phase $\theta$ determines the **azimuthal angle** on the equator.

---

## 🧮 The Inverse Quantum Fourier Transform (IQFT)

### What is QFT?

The **Quantum Fourier Transform** on $n$ qubits is defined:

$$\text{QFT}|j\rangle = \frac{1}{\sqrt{2^n}}\sum_{k=0}^{2^n-1} e^{2\pi i jk/2^n}|k\rangle$$

### What is IQFT (QFT†)?

The IQFT is the inverse:

$$\text{QFT}^\dagger\left(\frac{1}{\sqrt{2^n}}\sum_{k=0}^{2^n-1} e^{2\pi i \theta k}|k\rangle\right) \approx |2^n\theta\rangle$$

It "undoes" the Fourier transform, converting frequency-domain information back to position-domain.

### IQFT Circuit

```
|φ₀⟩ ──H──•──────────•───────•──────────────────
          │          │       │
|φ₁⟩ ─────⊕──H──•───⊕───────•──────────────────
                 │   │       │
|φ₂⟩ ────────────⊕───⊕──H───•──────────────────
                            │
...                         •──...──H──•─────────
                                       │
|φₙ₋₁⟩ ────────────────────────────────⊕──H─────

where •──⊕ represents controlled-phase rotations:
        R_k = |0⟩⟨0| ⊗ I + |1⟩⟨1| ⊗ (1  0     )
                                      (0  e^{iπ/2^{k}})
```

### Why IQFT Connects to Binary Representation

When $\theta$ can be written exactly as $\theta = 0.\phi_1\phi_2...\phi_n$ in binary:

$$\theta = \frac{\phi_1}{2} + \frac{\phi_2}{4} + \cdots + \frac{\phi_n}{2^n}$$

Then after phase encoding, the control register state becomes:

$$\frac{1}{\sqrt{2^n}}\left(|0\rangle + e^{2\pi i 0.\phi_n}|1\rangle\right) \otimes \left(|0\rangle + e^{2\pi i 0.\phi_{n-1}\phi_n}|1\rangle\right) \otimes \cdots \otimes \left(|0\rangle + e^{2\pi i 0.\phi_1\phi_2...\phi_n}|1\rangle\right)$$

The IQFT converts this **product state** back to the **computational basis state** $|\phi_1\phi_2...\phi_n\rangle$.

---

## 🎯 The Complete Algorithm: Pseudocode

```
function QPE(U, |ψ⟩, n):
    # U: unitary operator
    # |ψ⟩: eigenstate of U
    # n: number of control qubits (precision)

    # Initialize
    control = |0⟩^⊗ⁿ
    target = |ψ⟩

    # Step 1: Superposition
    control = H^⊗ⁿ(control)

    # Step 2: Phase encoding
    for k = 0 to n-1:
        control[k], target = C-U^{2^k}(control[k], target)

    # Step 3: Inverse QFT
    control = QFT^†(control)

    # Step 4: Measure
    φ = measure(control)

    # Return phase estimate
    θ̃ = φ / 2ⁿ
    return θ̃
```

---

## 📊 Resource Requirements

| Resource | Requirement | 
|----------|-------------|
| **Control qubits** | $n$ (determines precision) |
| **Target qubits** | $m$ (depends on $U$) |
| **Hadamard gates** | $n$ |
| **Controlled-$U^{2^k}$** | $n$ applications (exponential depth!) |
| **IQFT gates** | $O(n^2)$ |
| **Total depth** | $O(2^n + n^2)$ in the worst case |

> **⚠️ Challenges:** The controlled-$U^{2^k}$ operations require applying $U$ an exponential number of times. This is why QPE is mainly useful when $U$ can be implemented efficiently (e.g., as modular exponentiation in Shor's algorithm).

---

## 📝 Key Takeaways

1. **Hadamards create superposition** — all control qubits probe the phase simultaneously
2. **Controlled-unitaries encode the phase** — phase kickback transfers $\theta$ to the control register
3. **IQFT reads out the phase** — converts the phase-encoded state to a computational basis state
4. **Measurement yields the estimate** — $\tilde{\theta} = \tilde{\phi} / 2^n$
5. **Precision scales with $n$** — more qubits = more accurate estimation

---

## 🎯 Check Your Understanding

1. ❓ **Why do we apply $U^{2^k}$ instead of just $U$ for each control qubit?**
2. ❓ **What happens if $\theta$ cannot be expressed exactly in $n$ bits?**
3. ❓ **Trace through QPE for $n=2$ control qubits and $\theta = 0.25$.**
4. ❓ **Explain why the IQFT is needed — what would happen if we just measured directly after the controlled-unitaries?**
5. ❓ **What is the probability of getting the exact correct answer for a perfectly representable $\theta$?**

---

[[02 - Fundamental Concepts|← Previous: Fundamental Concepts]] | [[00 - QPE Study Guide Home|Study Guide]] | [[04 - Mathematical Derivations|Next: Mathematical Derivations →]]
