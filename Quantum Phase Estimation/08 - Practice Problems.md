# 08 — Practice Problems & Study Guide

> *"The only way to truly learn QPE is to work through problems yourself. This guide provides a structured path from basics to mastery."*

---

## 🎯 Study Session Plan

### Session 1: Conceptual Foundation (2 hours)

| Activity | Time | Topic |
|----------|------|-------|
| Read Modules 01-02 | 30 min | Introduction + Concepts |
| Watch NotebookLM Audio Overview | 20 min | Audio review of fundamentals |
| Answer Conceptual Questions | 40 min | Test basic understanding |
| Group Discussion | 30 min | Explain concepts to peers |

### Session 2: Mathematical & Algorithmic Depth (3 hours)

| Activity | Time | Topic |
|----------|------|-------|
| Read Module 03-04 | 45 min | Working Principle + Math |
| Work through derivations | 45 min | Derive key formulas yourself |
| Solve Numerical Problems | 60 min | Hand calculations |
| Group Problem Session | 30 min | Review solutions together |

### Session 3: Coding & Applications (3 hours)

| Activity | Time | Topic |
|----------|------|-------|
| Read Module 05 | 20 min | Applications |
| Run Qiskit Code (Module 07) | 60 min | Code and experiment |
| Modify and Explore | 40 min | Change parameters, analyze |
| Read Module 06 | 20 min | Challenges & Future |
| Group Discussion | 40 min | Present findings to research group |

### Session 4: Presentation Prep (2 hours)

| Activity | Time | Topic |
|----------|------|-------|
| Review Infographics (NotebookLM) | 15 min | Visual review |
| Create Presentation | 60 min | Build your PPT |
| Practice Q&A | 30 min | Anticipate questions |
| Dry Run | 15 min | Full presentation run |

---

## 📝 Conceptual Questions (Level 1: Foundation)

**1.** What is Quantum Phase Estimation and what problem does it solve?
**2.** Explain the difference between global and relative phase.
**3.** Why are eigenvalues of unitary operators always of the form $e^{2\pi i\theta}$?
**4.** What is phase kickback and why is it important for QPE?
**5.** Describe the roles of the control register and target register in QPE.
**6.** What does the Hadamard gate do in the QPE circuit?
**7.** Why do we apply $U^{2^k}$ instead of just $U$ for the $k$-th control qubit?
**8.** What is the role of the Inverse Quantum Fourier Transform in QPE?
**9.** How does measurement in QPE produce the estimated phase?
**10.** Name three major algorithms that use QPE as a subroutine.

---

## 📐 Numerical Problems (Level 2: Application)

### Problem 1: Eigenvalue Calculation
Given $U|\psi\rangle = e^{2\pi i \theta}|\psi\rangle$, find $\theta$ for each case:

(a) $U|\psi\rangle = -|\psi\rangle$
(b) $U|\psi\rangle = i|\psi\rangle$
(c) $U|\psi\rangle = e^{i\pi/4}|\psi\rangle$
(d) $U|\psi\rangle = \frac{1+i}{\sqrt{2}}|\psi\rangle$

<details>
<summary>Solution</summary>

(a) $e^{2\pi i\theta} = -1 \Rightarrow 2\pi\theta = \pi \Rightarrow \theta = 1/2$
(b) $e^{2\pi i\theta} = i \Rightarrow 2\pi\theta = \pi/2 \Rightarrow \theta = 1/4$
(c) $e^{2\pi i\theta} = e^{i\pi/4} \Rightarrow 2\pi\theta = \pi/4 \Rightarrow \theta = 1/8$
(d) $e^{2\pi i\theta} = \frac{1+i}{\sqrt{2}} = e^{i\pi/4} \Rightarrow \theta = 1/8$

</details>

### Problem 2: QPE with 2 Control Qubits
Consider QPE with $n=2$ control qubits and target $U|\psi\rangle = e^{2\pi i\theta}|\psi\rangle$.

(a) If $\theta = 0.25$, what is the exact measurement outcome?
(b) If $\theta = 0.3$, what is the probability of measuring each possible outcome?

<details>
<summary>Solution</summary>

(a) $2^n\theta = 4 \times 0.25 = 1$, so measurement yields $|01\rangle$ (binary for 1). 
   $\tilde{\theta} = 1/4 = 0.25$. Correct with 100% probability.

(b) $2^n\theta = 4 \times 0.3 = 1.2$. So $\phi = 1$ and $\delta = 0.2$.

$P(1) = \frac{\sin^2(\pi \times 0.2 \times 4)}{4^2 \sin^2(\pi \times 0.2)} = \frac{\sin^2(0.8\pi)}{16\sin^2(0.2\pi)}$

$\sin(0.8\pi) = \sin(0.2\pi) = \sin(36°) \approx 0.5878$

$P(1) = \frac{(0.5878)^2}{16(0.5878)^2} = \frac{1}{16} \approx 0.0625$

Wait, that doesn't seem right. Let me recalculate.

Actually, the formula is $P(\phi) = \frac{1}{2^{2n}} \left|\sum_{j=0}^{2^n-1} e^{2\pi i\delta j}\right|^2$

For $n=2$, $2^n = 4$:

$P(1) = \frac{1}{16} \left|1 + e^{2\pi i(0.2)} + e^{2\pi i(0.4)} + e^{2\pi i(0.6)}\right|^2$

Computing: $= \frac{1}{16}|1 + 0.309 + 0.951i - 0.809 + 0.588i - 0.809 - 0.588i|^2$

$= \frac{1}{16}|1 + 0.309 - 0.809 - 0.809 + i(0.951 + 0.588 - 0.588)|^2$

$= \frac{1}{16}|-0.309 + 0.951i|^2 = \frac{1}{16}(0.0955 + 0.904) = \frac{0.9995}{16} \approx 0.0625$

Hmm. $P(0) = \frac{1}{16}|1 + e^{0.8\pi i} + e^{1.6\pi i} + e^{2.4\pi i}|^2$ and $P(2) = P(0)$.

Wait, let me just compute directly:

$P(k) = \frac{1}{16} \frac{\sin^2(\pi(\theta - k/4) \cdot 4)}{\sin^2(\pi(\theta - k/4))}$ for $k = 0, 1, 2, 3$

For $\theta = 0.3$:
- $k=0$: $\Delta = 0.3$, $P = \frac{\sin^2(1.2\pi)}{16\sin^2(0.3\pi)}$
- $k=1$: $\Delta = 0.05$, $P = \frac{\sin^2(0.2\pi)}{16\sin^2(0.05\pi)}$
- $k=2$: $\Delta = -0.2$, $P = \frac{\sin^2(-0.8\pi)}{16\sin^2(-0.2\pi)} = \frac{\sin^2(0.8\pi)}{16\sin^2(0.2\pi)}$
- $k=3$: $\Delta = -0.45$, $P = \frac{\sin^2(-1.8\pi)}{16\sin^2(-0.45\pi)} = \frac{\sin^2(1.8\pi)}{16\sin^2(0.45\pi)}$

Computing numerically:
- $P(0)$: $\sin(1.2\pi) = \sin(216°) = -0.5878$, $\sin^2 = 0.3455$; $\sin(0.3\pi) = \sin(54°) = 0.809$, $\sin^2 = 0.6545$; $P(0) = 0.3455/(16 \cdot 0.6545) = 0.0330$ 
- $P(1)$: $\sin(0.2\pi) = \sin(36°) = 0.5878$, $\sin^2 = 0.3455$; $\sin(0.05\pi) = \sin(9°) = 0.1564$, $\sin^2 = 0.0245$; $P(1) = 0.3455/(16 \cdot 0.0245) = 0.881$
- $P(2)$: $\sin(0.8\pi) = \sin(144°) = 0.5878$, $\sin^2 = 0.3455$; $\sin(0.2\pi) = 0.5878$, $\sin^2 = 0.3455$; $P(2) = 0.3455/(16 \cdot 0.3455) = 0.0625$
- $P(3)$: $\sin(1.8\pi) = \sin(324°) = -0.5878$, $\sin^2 = 0.3455$; $\sin(0.45\pi) = \sin(81°) = 0.9877$, $\sin^2 = 0.9755$; $P(3) = 0.3455/(16 \cdot 0.9755) = 0.0221$

Check sum: $0.0330 + 0.881 + 0.0625 + 0.0221 = 0.9986 \approx 1$ ✅

So the most likely outcome is $k=1$, giving $\tilde{\theta} = 1/4 = 0.25$ with 88.1% probability.

</details>

### Problem 3: Error Analysis
For QPE with $n=4$ control qubits and $\theta = 0.37$:

(a) What is the closest representable value?
(b) What is the probability of measuring this closest value?
(c) How many extra qubits are needed for 99% success probability?

<details>
<summary>Solution</summary>

(a) $2^4 \times 0.37 = 5.92$, closest integer is $6$. Best estimate: $6/16 = 0.375$.
   $\delta = 0.37 - 0.375 = -0.005$ (or $0.37 - 6/16 = 0.37 - 0.375 = -0.005$).

(b) $P = \frac{\sin^2(\pi \times 0.005 \times 16)}{256 \cdot \sin^2(\pi \times 0.005)} = \frac{\sin^2(0.08\pi)}{256\sin^2(0.005\pi)}$
   
   $\sin(0.08\pi) = \sin(14.4°) \approx 0.2487$
   $\sin(0.005\pi) = \sin(0.9°) \approx 0.0157$
   
   $P = \frac{(0.2487)^2}{256 \times (0.0157)^2} = \frac{0.06185}{256 \times 0.000246} = \frac{0.06185}{0.0630} \approx 0.982$

So ~98.2% probability of measuring $k=6$ (closest integer).

(c) For $\epsilon = 0.01$, we need $t = \lceil \log_2(2 + 1/(2\epsilon))\rceil = \lceil \log_2(2 + 50)\rceil = \lceil \log_2(52)\rceil = 6$ extra qubits.
   Total: $n + t = 4 + 6 = 10$ control qubits for 99% success probability.

</details>

### Problem 4: Phase Kickback Matrix
Write the matrix representation of the controlled-$U$ gate where $U = \begin{pmatrix} 1 & 0 \\ 0 & e^{2\pi i\theta} \end{pmatrix}$.

<details>
<summary>Solution</summary>

$\text{C-}U = |0\rangle\langle 0| \otimes I + |1\rangle\langle 1| \otimes U$

$= \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix} \otimes \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} + \begin{pmatrix} 0 & 0 \\ 0 & 1 \end{pmatrix} \otimes \begin{pmatrix} 1 & 0 \\ 0 & e^{2\pi i\theta} \end{pmatrix}$

$= \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & e^{2\pi i\theta} \end{pmatrix}$

</details>

---

## 💻 Coding Problems (Level 3: Programming)

### Problem 5: Implement QPE from Scratch
Write a complete QPE function in Qiskit that:
1. Takes $U$ (as a gate), $n$ (control qubits), and initial state $|\psi\rangle$ as inputs
2. Implements the full QPE circuit
3. Returns the estimated phase $\tilde{\theta}$
4. Calculates the error $|\tilde{\theta} - \theta|$

<details>
<summary>Template</summary>

```python
def my_qpe(U_gate, n_control, init_state, theta_true=None):
    # Your code here
    # 1. Create circuit
    # 2. Prepare initial state
    # 3. Hadamards on control
    # 4. Controlled-U^{2^k}
    # 5. IQFT
    # 6. Measure
    # 7. Simulate and extract phase
    pass
```
</details>

### Problem 6: Explore Precision Scaling
Create a plot showing how QPE precision scales with $n$:

```python
# Template
import matplotlib.pyplot as plt
import numpy as np

theta_true = 1/np.pi  # Not exactly representable
n_values = range(2, 11)
errors = []

for n in n_values:
    # Run QPE with n control qubits
    # Record error
    pass

plt.plot(n_values, errors, 'o-')
plt.yscale('log')
plt.xlabel('Number of control qubits (n)')
plt.ylabel('Estimation error')
plt.grid(True)
plt.show()
```

### Problem 7: Phase Kickback for XOR
Create a circuit that demonstrates phase kickback for a CNOT gate (XOR in the computational basis):

```python
# CNOT: Controlled-NOT (XOR)
# |c⟩|t⟩ → |c⟩|c ⊕ t⟩
# Find: CNOT eigenstates and their eigenvalues
```

<details>
<summary>Hint</summary>

The CNOT eigenstates are $|+\rangle|0\rangle$ and $|-\rangle|1\rangle$ with eigenvalues $+1$ and $-1$.

$CNOT|+\rangle|0\rangle = |+\rangle|0\rangle$
$CNOT|-\rangle|1\rangle = -|-\rangle|1\rangle$

Can you see why?
</details>

### Problem 8: Noisy QPE Simulation
Add different noise models and see how QPE degrades:

```python
from qiskit.providers.aer.noise import (
    NoiseModel, 
    phase_amplitude_damping_error,
    depolarizing_error,
    thermal_relaxation_error
)

# Try each noise type and compare results
```

---

## 🧩 Group Discussion Questions

### For Your Research Group Presentation

**1. "Why is QPE considered the most important quantum subroutine?"**
- Discuss the range of applications
- Compare to classical analog (FFT)
- Why can't classical computers do this?

**2. "How close are we to running useful QPE on real hardware?"**
- Current state-of-the-art
- IQPE vs. standard QPE
- What breakthroughs are needed?

**3. "Which application will reach quantum advantage first — factoring, chemistry, or materials science?"**
- Technical feasibility
- Economic impact
- Timeline estimates

**4. "How does QPE relate to the broader field of quantum sensing and metrology?"**
- Similarities in phase estimation
- Different noise environments
- Cross-pollination of ideas

**5. "What would you work on if you were a quantum algorithm researcher today?"**
- Error mitigation for QPE
- New applications
- Hardware-algorithm codesign

---

## 📝 Presentation Outline Template

Here's a suggested structure for your research group PPT:

### Slide 1: Title
- "Quantum Phase Estimation: Theory, Applications, and Future Prospects"
- Your name, research group, date

### Slide 2: Outline
- What is QPE? → How it Works → Math → Applications → Challenges → Demo

### Slide 3: Motivation
- Why phase matters in quantum systems
- Classical vs. quantum phase estimation

### Slide 4: The QPE Problem
- $U|\psi\rangle = e^{2\pi i\theta}|\psi\rangle$
- Find $\theta$

### Slide 5: QPE Circuit (Diagram)
- Show the full circuit

### Slide 6: Phase Kickback Explanation
- Interactive demonstration

### Slide 7: Step-by-Step Walkthrough
- Hadamard → Controlled-U → IQFT → Measurement

### Slide 8: The Math
- Key equations (keep it clean!)

### Slide 9: Applications
- Shor's, Chemistry, Materials, HHL

### Slide 10: Demo (if possible)
- Run a QPE circuit and show results

### Slide 11: Challenges
- NISQ limitations, error correction, resources

### Slide 12: Future Outlook
- Roadmap, IQPE, hybrid approaches

### Slide 13: Key Takeaways
- Top 3 things to remember

### Slide 14: Q&A
- Be prepared for these questions...

---

## 🎤 Anticipated Q&A Questions

Be ready for these from your research group:

| Question | Key Points to Cover |
|----------|-------------------|
| "Why can't we just measure the phase directly?" | Phase is a rotation — measuring collapses the state. QPE uses indirect inference. |
| "How does IQPE differ from standard QPE?" | 1 control qubit, iterative measurement, more NISQ-friendly |
| "What's the role of the eigenstate?" | The eigenstate provides the "reference frame" for phase measurement |
| "What happens with a bad initial state?" | Lower success probability, need more runs |
| "Can QPE run on current hardware?" | Very limited — needs error correction for useful problems |
| "What's the relationship to the Fourier transform?" | IQFT is the quantum version of the inverse DFT — it finds the frequency (phase) |
| "How many qubits needed for useful chemistry?" | 100-200 logical qubits → millions of physical qubits with error correction |
| "Is Shor's algorithm really a threat to RSA?" | Yes — but fault-tolerant quantum computers are likely 10-15 years away |

---

## 📊 Self-Assessment Rubric

| Level | Can You... | Check |
|-------|-----------|-------|
| 🟢 **Basic** | Explain what QPE does in one sentence? | ☐ |
| 🟢 **Basic** | Draw the QPE circuit? | ☐ |
| 🟢 **Basic** | Explain phase kickback? | ☐ |
| 🟡 **Intermediate** | Derive the probability formula? | ☐ |
| 🟡 **Intermediate** | Code QPE in Qiskit? | ☐ |
| 🟡 **Intermediate** | Explain non-exact phase behavior? | ☐ |
| 🟠 **Advanced** | Derive the error bounds? | ☐ |
| 🟠 **Advanced** | Implement IQPE? | ☐ |
| 🟠 **Advanced** | Explain Shor's use of QPE? | ☐ |
| 🔴 **Expert** | Design a new QPE variant? | ☐ |
| 🔴 **Expert** | Analyze noise resilience? | ☐ |
| 🔴 **Expert** | Connect QPE to quantum metrology? | ☐ |

**Target for your presentation:** 🟡 Intermediate level

---

## 📚 Quick Revision Cards

### Card 1: QPE Problem
```
Given: U|ψ⟩ = e^{2πiθ}|ψ⟩
Find: θ (the phase)
```

### Card 2: Circuit Steps
```
|0⟩⊗ⁿ —H⊗ⁿ—•——•——•——IQFT— M
            |   |   |
|ψ⟩ ———————U——U²——U⁴—
```

### Card 3: Key Formula
```math
P(ϕ) = sin²(πδ·2ⁿ) / (2²ⁿ · sin²(πδ))
```

### Card 4: Phase Kickback
```
C-U(|0⟩+|1⟩)|ψ⟩ = (|0⟩+e^{2πiθ}|1⟩)|ψ⟩
```

### Card 5: Minimum Success
```
P_min = 4/π² ≈ 40.5% (worst case)
Boosts with t extra qubits: 1 - 1/2^(t-1)
```

---

[[07 - QPE Code Examples|← Previous: Code Examples]] | [[00 - QPE Study Guide Home|← Back to Study Guide]]
