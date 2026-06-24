# 02 — Fundamental Concepts Behind QPE

> *Before we can understand QPE, we need to master the building blocks: qubits, superposition, unitary operators, eigenstates, and quantum phases.*

---

## 1️⃣ Qubits, Superposition, and Quantum States

### The Qubit

A **qubit** is the fundamental unit of quantum information. Unlike a classical bit (0 or 1), a qubit can exist in a **superposition** of states.

**Mathematical representation:**

$$|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$$

where:
- $\alpha, \beta \in \mathbb{C}$ are **complex amplitudes**
- $|\alpha|^2 + |\beta|^2 = 1$ (normalization condition)
- $|0\rangle = \begin{pmatrix}1\\0\end{pmatrix}$ and $|1\rangle = \begin{pmatrix}0\\1\end{pmatrix}$

### 📐 The Bloch Sphere

Every single-qubit state can be visualized on the **Bloch sphere**. The phase determines the azimuthal angle on the equator:

![[Diagrams/09_bloch_sphere_phases.png]]

The general state on the Bloch sphere:

$$|\psi\rangle = \cos\frac{\theta}{2}|0\rangle + e^{i\phi}\sin\frac{\theta}{2}|1\rangle$$

Where $\theta$ is the polar angle and $\phi$ is the azimuthal angle — **this $\phi$ is the quantum phase!**

### Superposition

Superposition is the ability of a qubit to be in **both** $|0\rangle$ and $|1\rangle$ simultaneously.

**Example:** The Hadamard gate creates superposition:
$$H|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$$

This is like a coin spinning in the air — it's neither heads nor tails until it lands (is measured).

### Multiple Qubits

For $n$ qubits, the state is a vector in a $2^n$-dimensional Hilbert space:

$$|\psi\rangle = \sum_{x \in \{0,1\}^n} c_x |x\rangle$$

where $\sum_x |c_x|^2 = 1$.

> **💡 Key Insight:** $n$ qubits can store information in $2^n$ amplitudes — this is where quantum computers get their power!

---

## 2️⃣ Unitary Operators and Eigenstates

### Unitary Operators

A **unitary operator** $U$ is the quantum equivalent of a "reversible operation." 

**Definition:** $U$ is unitary if:
$$U^\dagger U = UU^\dagger = I$$

where $U^\dagger$ is the **conjugate transpose** (Hermitian conjugate) of $U$.

**Properties:**
- Unitary operations **preserve norm**: $\langle\psi|\psi\rangle = \langle\psi|U^\dagger U|\psi\rangle = 1$
- Unitary operations are **reversible**: $U^{-1} = U^\dagger$
- All quantum gates are unitary
- Unitary operators have eigenvalues of magnitude 1

**Examples of unitary operators:**

| Gate | Matrix | Action |
|------|--------|--------|
| Hadamard $H$ | $\frac{1}{\sqrt{2}}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$ | Creates superposition |
| Pauli-X | $\begin{pmatrix}0&1\\1&0\end{pmatrix}$ | Quantum NOT gate |
| Pauli-Z | $\begin{pmatrix}1&0\\0&-1\end{pmatrix}$ | Phase flip |
| Phase $S$ | $\begin{pmatrix}1&0\\0&i\end{pmatrix}$ | 90° rotation |
| T-gate | $\begin{pmatrix}1&0\\0&e^{i\pi/4}\end{pmatrix}$ | 45° rotation |

### Eigenstates and Eigenvalues

For a unitary operator $U$, an **eigenstate** $|\psi\rangle$ satisfies:

$$U|\psi\rangle = \lambda |\psi\rangle$$

where $\lambda$ is the **eigenvalue**. Because $U$ is unitary:

$$|\lambda|^2 = 1 \quad \Rightarrow \quad \lambda = e^{2\pi i \theta}$$

This is **critical** — the eigenvalue is always a phase on the unit circle!

### 🔍 Why This Matters for QPE

QPE answers: *"Given $U$ and its eigenstate $|\psi\rangle$, what is $\theta$?"*

$$U|\psi\rangle = e^{2\pi i \theta} |\psi\rangle$$

Think of it like this:
- $U$ is a "black box" operation
- $|\psi\rangle$ is a state that doesn't change (up to a global phase) when $U$ is applied
- The eigenvalue $e^{2\pi i\theta}$ tells us the "rotation amount"

### Finding $e^{2\pi i \theta}$: The Circle

```
                 Im(λ)
                   ▲
                   │
     e^{2πi·¾}    │    e^{2πi·¼}
     λ = -i       │    λ = i
          ✦       │       ✦
                   │
    ✦──────────────┼──────────────✦──► Re(λ)
     λ = -1       │       λ = 1
     e^{2πi·½}   │      e^{2πi·0}
                   │
        ✦         │       ✦
     e^{2πi·⅝}   │    e^{2πi·⅛}
                   │
                   ▼
```

The phase $\theta$ tells us **where on the circle** the eigenvalue lies.

---

## 3️⃣ Quantum Phases and Their Significance

### What is a Quantum Phase?

A **quantum phase** is the angle $\phi$ in the complex exponential:

$$e^{i\phi} = \cos\phi + i\sin\phi$$

### Global vs. Relative Phase

**Global Phase:** 
$$|\psi\rangle \quad \text{vs.} \quad e^{i\phi}|\psi\rangle$$

These are physically **indistinguishable** — all measurement probabilities are the same.

**Relative Phase:**
$$\frac{|0\rangle + |1\rangle}{\sqrt{2}} \quad \text{vs.} \quad \frac{|0\rangle + e^{i\phi}|1\rangle}{\sqrt{2}}$$

These are **physically different** — relative phases affect interference!

### Why Phases Matter

**1. Interference**

When two quantum states combine, their phases determine if they add (constructive) or cancel (destructive):

$$|\psi_1\rangle + |\psi_2\rangle = \alpha_1|0\rangle + \alpha_2|0\rangle = (\alpha_1 + \alpha_2)|0\rangle$$

If $\alpha_1 = \frac{1}{\sqrt{2}}$ and $\alpha_2 = -\frac{1}{\sqrt{2}}$, they cancel completely!

### Phase Kickback (The Heart of QPE)

This is the most important concept for QPE. Consider a controlled-$U$ gate:

![[Diagrams/01b_phase_kickback_circuit.png]]

```
|0⟩ —●—   If control is |0⟩, nothing happens
     |    If control is |1⟩, U is applied
|ψ⟩ —U—
```

Now, if $|\psi\rangle$ is an eigenstate of $U$ with $U|\psi\rangle = e^{2\pi i\theta}|\psi\rangle$:

$$\text{Controlled-}U (|0\rangle \otimes |\psi\rangle) = |0\rangle \otimes |\psi\rangle$$
$$\text{Controlled-}U (|1\rangle \otimes |\psi\rangle) = |1\rangle \otimes e^{2\pi i\theta}|\psi\rangle = e^{2\pi i\theta} |1\rangle \otimes |\psi\rangle$$

The phase "kicks back" to the control qubit! If the control is in superposition:

$$H|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$$

Then:
$$\text{C-}U\left(\frac{|0\rangle + |1\rangle}{\sqrt{2}} \otimes |\psi\rangle\right) = \frac{|0\rangle + e^{2\pi i\theta}|1\rangle}{\sqrt{2}} \otimes |\psi\rangle$$

**The phase $e^{2\pi i\theta}$ has been transferred to the control qubit!** This is phase kickback, and it's the foundation of QPE.

### The Phase Estimation Problem (Formal)

Given:
- A unitary operator $U$ acting on $m$ qubits
- An eigenstate $|\psi\rangle$ such that $U|\psi\rangle = e^{2\pi i\theta}|\psi\rangle$
- Access to controlled-$U^{2^k}$ operations

**Goal:** Estimate $\theta$ to $n$ bits of precision with high confidence.

---

## 📊 Summary Table: Key Concepts

| Concept | Definition | Why It Matters for QPE |
|---------|------------|----------------------|
| **Qubit** | $\\alpha|0\\rangle + \\beta|1\\rangle$ | The basic unit; QPE uses two registers of qubits |
| **Superposition** | Being in multiple states at once | Allows parallel phase estimation |
| **Unitary Operator** | $U^\\dagger U = I$ | The operator whose eigenvalue we're finding |
| **Eigenstate** | $U|\\psi\\rangle = \\lambda|\\psi\\rangle$ | The state that doesn't change under $U$ |
| **Eigenvalue** | $\\lambda = e^{2\\pi i \\theta}$ | Contains the phase we want to estimate |
| **Phase** | $e^{i\\phi}$ | Encodes energy, frequency, rotation |
| **Phase Kickback** | Phase transfers to control qubit | The mechanism QPE uses to "read" the phase |

---

## 🎯 Check Your Understanding

1. ❓ **Why are eigenvalues of unitary operators always of the form $e^{i\theta}$?**
2. ❓ **What's the difference between global and relative phase?**
3. ❓ **Explain phase kickback in your own words.**
4. ❓ **If $U|\\psi\\rangle = e^{2\\pi i(0.75)}|\\psi\\rangle$, what is the eigenvalue?**

**Interactive Exercise:** Write down the state $\frac{|0\\rangle + e^{i\\pi/3}|1\\rangle}{\sqrt{2}}$ and compute its measurement probabilities. How does the phase affect the result?

---

[[01 - Introduction to QPE|← Previous: Introduction]] | [[00 - QPE Study Guide Home|Study Guide]] | [[03 - Working Principle of QPE|Next: Working Principle →]]
