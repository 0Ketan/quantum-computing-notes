# 04 — Mathematical Derivations for QPE

> *"To truly understand QPE, you must master the mathematics. This note provides every derivation step-by-step."*

---

## 📐 Notation Reference

| Symbol | Meaning |
|--------|---------|
| $\\mathbb{C}$ | Complex numbers |
| $\\mathcal{H}$ | Hilbert space |
| $\\langle \\psi |$ | Bra (row vector, conjugate transpose) |
| $| \\psi \\rangle$ | Ket (column vector) |
| $\\langle \\phi | \\psi \\rangle$ | Inner product |
| $U^\\dagger$ | Hermitian conjugate of $U$ |
| $\\otimes$ | Tensor product |
| $|x\\rangle$ | Computational basis state |
| $\\mathbb{I}$ | Identity operator |
| $e^{i\\theta}$ | Complex exponential |

---

## 1️⃣ Derivation: Phase Kickback

### The Fundamental Identity

Let $U$ be a unitary operator with eigenstate $|\psi\rangle$:

$$U|\psi\rangle = e^{2\pi i\theta}|\psi\rangle$$

Consider the controlled-$U$ gate:

$$\text{C-}U = |0\rangle\langle 0| \otimes \mathbb{I} + |1\rangle\langle 1| \otimes U$$

**Proof of phase kickback:**

$$\text{C-}U(|c\rangle \otimes |\psi\rangle) = \begin{cases}
|0\rangle \otimes |\psi\rangle & \text{if } c = 0 \\
|1\rangle \otimes U|\psi\rangle = e^{2\pi i\theta} |1\rangle \otimes |\psi\rangle & \text{if } c = 1
\end{cases}$$

For a control qubit in superposition $|c\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$:

$$\text{C-}U\left(\frac{|0\rangle + |1\rangle}{\sqrt{2}} \otimes |\psi\rangle\right) = \frac{|0\rangle|\psi\rangle + e^{2\pi i\theta}|1\rangle|\psi\rangle}{\sqrt{2}}$$

$$= \frac{|0\rangle + e^{2\pi i\theta}|1\rangle}{\sqrt{2}} \otimes |\psi\rangle$$

**The phase has "kicked back" to the control qubit.** ✅

### Generalization to $n$ Control Qubits

For the $k$-th control qubit (counting from 0), we apply controlled-$U^{2^k}$:

$$\text{C-}U^{2^k} \left(\frac{|0\rangle + |1\rangle}{\sqrt{2}} \otimes |\psi\rangle\right) = \frac{|0\rangle + e^{2\pi i \theta \cdot 2^k}|1\rangle}{\sqrt{2}} \otimes |\psi\rangle$$

After all $n$ controlled operations on the initial superposition:

$$|\Psi\rangle = \frac{1}{\sqrt{2^n}} \sum_{j=0}^{2^n-1} e^{2\pi i \theta j} |j\rangle \otimes |\psi\rangle$$

**Proof by induction:**

Base case: $n=1$, we already proved this above.

Inductive step: Assume it holds for $n$ qubits. For $n+1$, we have the $n$-qubit state plus one more qubit:

The new qubit applies $U^{2^n}$, contributing a factor $e^{2\pi i \theta \cdot 2^n \cdot j_{n+1}}$ where $j_{n+1} \in \{0,1\}$. This gives:

$$|\Psi_{n+1}\rangle = \frac{1}{\sqrt{2^{n+1}}}\sum_{j_{n+1}=0}^{1}\sum_{j=0}^{2^n-1} e^{2\pi i\theta(j + 2^n j_{n+1})} |j_{n+1}, j\rangle \otimes |\psi\rangle$$

$$= \frac{1}{\sqrt{2^{n+1}}}\sum_{k=0}^{2^{n+1}-1} e^{2\pi i\theta k} |k\rangle \otimes |\psi\rangle$$

where $k = j + 2^n j_{n+1}$. ✅

---

## 2️⃣ Derivation: The Quantum Fourier Transform (QFT)

### Definition

The QFT on $n$ qubits is defined by its action on a computational basis state $|j\rangle$:

$$\text{QFT}|j\rangle = \frac{1}{\sqrt{2^n}} \sum_{k=0}^{2^n-1} e^{2\pi i jk/2^n} |k\rangle$$

### Matrix Form

The QFT matrix is:

$$F_{jk} = \frac{1}{\sqrt{2^n}} \omega^{jk}$$

where $\omega = e^{2\pi i / 2^n}$ is the $2^n$-th root of unity and $j,k \in \{0,1,\ldots,2^n-1\}$.

### Product Representation

Using binary expansion: $j = j_1j_2\ldots j_n$ where $j = j_1 2^{n-1} + j_2 2^{n-2} + \cdots + j_n 2^0$.

Also define: $0.j_l j_{l+1} \ldots j_n = \frac{j_l}{2} + \frac{j_{l+1}}{4} + \cdots + \frac{j_n}{2^{n-l+1}}$

Then the QFT can be written as:

$$\text{QFT}|j\rangle = \frac{1}{\sqrt{2^n}} \bigotimes_{l=1}^n \left(|0\rangle + e^{2\pi i \, 0.j_l j_{l+1}\ldots j_n}|1\rangle\right)$$

### Inverse QFT (IQFT)

The IQFT is the inverse:

$$\text{QFT}^\dagger = \text{QFT}^{-1}$$

Matrix element: $(F^{-1})_{jk} = \frac{1}{\sqrt{2^n}} \omega^{-jk}$

**Key property:** $\text{QFT}^\dagger \cdot \text{QFT} = \mathbb{I}$

### Proof of Unitarily (that QFT preserves norm)

For any state $|\phi\rangle = \sum_j c_j |j\rangle$:

$$\|\text{QFT}|\phi\rangle\|^2 = \langle\phi|\text{QFT}^\dagger \text{QFT}|\phi\rangle = \langle\phi|\phi\rangle = \sum_j |c_j|^2 = 1$$

---

## 3️⃣ Derivation: Why QPE Works (The Full Proof)

### Setup

We have $n$ control qubits and state $|\psi\rangle$ where $U|\psi\rangle = e^{2\pi i\theta}|\psi\rangle$.

After Step 2 (Hadamard + controlled-unitaries):

$$|\Psi_2\rangle = \frac{1}{\sqrt{2^n}} \sum_{j=0}^{2^n-1} e^{2\pi i\theta j} |j\rangle \otimes |\psi\rangle$$

### Key Insight

This is exactly $\text{QFT}|2^n\theta\rangle$ (when $2^n\theta$ is an integer)!

Let's verify:

$$\text{QFT}|\phi\rangle = \frac{1}{\sqrt{2^n}} \sum_{k=0}^{2^n-1} e^{2\pi i \phi k / 2^n} |k\rangle$$

For $\phi = 2^n\theta$:

$$\text{QFT}|2^n\theta\rangle = \frac{1}{\sqrt{2^n}} \sum_{k=0}^{2^n-1} e^{2\pi i (2^n\theta)k/2^n} |k\rangle = \frac{1}{\sqrt{2^n}} \sum_{k=0}^{2^n-1} e^{2\pi i \theta k} |k\rangle$$

This matches our $|\Psi_2\rangle$ (up to the tensor product with $|\psi\rangle$). ✅

### Applying the IQFT

$$|\Psi_3\rangle = (\text{QFT}^\dagger \otimes \mathbb{I}) |\Psi_2\rangle$$

**Case 1: $\theta = \phi / 2^n$ where $\phi$ is an integer (exact representation)**

$$|\Psi_2\rangle = \text{QFT}|\phi\rangle \otimes |\psi\rangle$$
$$|\Psi_3\rangle = \text{QFT}^\dagger \text{QFT}|\phi\rangle \otimes |\psi\rangle = |\phi\rangle \otimes |\psi\rangle$$

Measurement yields $\phi$ with 100% probability. $\tilde{\theta} = \phi/2^n = \theta$ exactly. ✅

**Case 2: $\theta$ is not exactly representable in $n$ bits**

Let $\theta = \frac{\phi}{2^n} + \delta$ where $\phi = \lfloor 2^n\theta\rfloor$ and $0 < |\delta| < \frac{1}{2^{n+1}}$.

$$|\Psi_2\rangle = \frac{1}{\sqrt{2^n}} \sum_{j=0}^{2^n-1} e^{2\pi i (\phi/2^n + \delta) j} |j\rangle \otimes |\psi\rangle$$

$$= \frac{1}{\sqrt{2^n}} \sum_{j=0}^{2^n-1} e^{2\pi i \phi j/2^n} e^{2\pi i \delta j} |j\rangle \otimes |\psi\rangle$$

After IQFT:

$$|\Psi_3\rangle = \frac{1}{2^n}\sum_{k=0}^{2^n-1} \sum_{j=0}^{2^n-1} e^{-2\pi i kj/2^n} e^{2\pi i (\phi/2^n + \delta)j} |k\rangle \otimes |\psi\rangle$$

Probability of measuring $k$:

$$P(k) = \left|\frac{1}{2^n}\sum_{j=0}^{2^n-1} e^{2\pi i(\phi - k)j/2^n} e^{2\pi i\delta j}\right|^2$$

---

## 4️⃣ Derivation: Error Bounds and Success Probability

### Probability of Correct Answer

The probability of measuring $\phi = \lfloor 2^n\theta\rfloor$ (the closest integer) is:

$$P(\phi) = \frac{1}{2^{2n}} \left|\sum_{j=0}^{2^n-1} e^{2\pi i (\delta)j}\right|^2$$

This is a **geometric series**! Let $r = e^{2\pi i\delta}$:

$$\sum_{j=0}^{2^n-1} r^j = \frac{1 - r^{2^n}}{1 - r}$$

So:

$$P(\phi) = \frac{1}{2^{2n}} \left|\frac{1 - e^{2\pi i \delta 2^n}}{1 - e^{2\pi i \delta}}\right|^2$$

### Simplifying with Trigonometric Identities

Using $|1 - e^{i\alpha}|^2 = 4\sin^2(\alpha/2)$:

$$P(\phi) = \frac{1}{2^{2n}} \frac{\sin^2(\pi \delta 2^n)}{\sin^2(\pi \delta)}$$

### Worst-Case Bound

The worst case is when $\delta = \frac{1}{2^{n+1}}$ (equidistant between two integers):

$$P(\phi) \geq \frac{4}{\pi^2} \approx 0.405$$

**Proof of the bound:** For $0 \leq \delta \leq \frac{1}{2^{n+1}}$, we have $\sin(\pi \delta 2^n) \geq 2\delta 2^n$ (using $\sin x \geq \frac{2}{\pi}x$ for $0 \leq x \leq \pi/2$) and $\sin(\pi\delta) \leq \pi\delta$. 

$$P(\phi) \geq \frac{1}{2^{2n}} \frac{(2\delta 2^n)^2}{(\pi\delta)^2} = \frac{4}{\pi^2}$$ ✅

### Boosting Success Probability

To succeed with probability at least $1-\epsilon$, use:

$$n + \left\lceil \log_2\left(2 + \frac{1}{2\epsilon}\right) \right\rceil$$

control qubits. The extra qubits (beyond the $n$ needed for precision) reduce the probability of error exponentially.

**Example:** For $\epsilon = 0.01$ (99% success), we need:
$$\lceil \log_2(2 + 50)\rceil = \lceil \log_2(52)\rceil = 6$$

extra qubits. So $n+6$ qubits total for $n$-bit precision with 99% confidence.

---

## 5️⃣ Derivation: The Controlled-Unitary and Modular Exponentiation

### For $U^{2^k}$

$$U^{2^k}|\psi\rangle = (e^{2\pi i\theta})^{2^k}|\psi\rangle = e^{2\pi i\theta \cdot 2^k}|\psi\rangle$$

### Implementation via Repeated Squaring

To implement $U^{2^k}$ efficiently, we can use **repeated squaring**:

$$U^{2^k} = (U^{2^{k-1}})^2$$

This requires only $k$ squaring operations, not $2^k$ direct applications.

---

## 6️⃣ Derivation: Connecting QPE to the Fourier Transform (Classical Analogy)

### Classical Fourier Transform

The discrete Fourier transform (DFT) of a sequence $x_0, x_1, \ldots, x_{N-1}$:

$$X_k = \frac{1}{\sqrt{N}}\sum_{j=0}^{N-1} x_j e^{-2\pi i jk/N}$$

### The QPE Connection

In QPE, our state after phase encoding is:

$$\frac{1}{\sqrt{2^n}}\sum_{j=0}^{2^n-1} e^{2\pi i\theta j}|j\rangle$$

This is analogous to having $x_j = e^{2\pi i\theta j}$ — a **pure tone** at frequency $\theta$.

The IQFT computes:

$$X_k = \frac{1}{\sqrt{2^n}}\sum_{j=0}^{2^n-1} e^{2\pi i\theta j} e^{-2\pi i kj/2^n} = \frac{1}{\sqrt{2^n}}\sum_{j=0}^{2^n-1} e^{2\pi i(\theta - k/2^n)j}$$

This peaks when $k/2^n \approx \theta$, i.e., $k \approx 2^n\theta$. **The IQFT finds the frequency!**

---

## 7️⃣ Derivation: Eigenvalue Estimation with Matrix Analysis

### Why All Unitary Eigenvalues Have Magnitude 1

If $U$ is unitary ($U^\dagger U = I$) and $|\psi\rangle$ is an eigenvector:

$$U|\psi\rangle = \lambda|\psi\rangle$$
$$\langle\psi|U^\dagger U|\psi\rangle = \langle\psi|\psi\rangle = 1$$
$$\langle\psi|U^\dagger U|\psi\rangle = |\lambda|^2 \langle\psi|\psi\rangle = |\lambda|^2$$

Therefore $|\lambda|^2 = 1$, so $\lambda = e^{i\phi}$ for some real $\phi$. ✅

### Phase in Terms of the Hamiltonian

For a Hamiltonian $H$ (Hermitian matrix):

$$U(t) = e^{-iHt/\hbar}$$

If $H|E\rangle = E|E\rangle$, then:

$$U(t)|E\rangle = e^{-iEt/\hbar}|E\rangle$$

So the phase $\theta = -\frac{Et}{2\pi\hbar}$. Measuring $\theta$ gives us the energy $E$.

---

## 🧮 Formula Reference Card

| Formula | Description |
|---------|-------------|
| $U\\|\\psi\\rangle = e^{2\\pi i\\theta}\\|\\psi\\rangle$ | Eigenvalue equation |
| $H\\|0\\rangle = \\frac{\\|0\\rangle + \\|1\\rangle}{\\sqrt{2}}$ | Hadamard creates superposition |
| $\\text{C-}U = \\|0\\rangle\\langle 0\\| \\otimes \\mathbb{I} + \\|1\\rangle\\langle 1\\| \\otimes U$ | Controlled-U gate |
| $\\frac{1}{\\sqrt{2^n}}\\sum_{j=0}^{2^n-1} e^{2\\pi i\\theta j}\\|j\\rangle$ | State after phase encoding |
| $\\text{QFT}\\|j\\rangle = \\frac{1}{\\sqrt{2^n}}\\sum_{k=0}^{2^n-1} \\omega^{jk}\\|k\\rangle$ | QFT definition |
| $\\frac{\\sin^2(\\pi\\delta 2^n)}{2^{2n}\\sin^2(\\pi\\delta)}$ | Probability of correct result |
| $\\frac{4}{\\pi^2} \\approx 0.405$ | Minimum success probability (n qubits) |

---

## ✍️ Practice: Derive These Yourself

1. **Derive the probability formula** $P(\\phi) = \\frac{\\sin^2(\\pi\\delta 2^n)}{2^{2n}\\sin^2(\\pi\\delta)}$ from first principles
2. **Prove** that the QFT matrix is unitary
3. **Show** that $\\text{QFT}^\\dagger = \\text{QFT}^{-1}$ by computing $\\sum_k (F^\\dagger)_{ik}F_{kj}$
4. **Derive** why adding $t$ extra qubits gives success probability $1 - \\frac{1}{2^{t-1}}$
5. **Compute** the probability of measuring the exact answer for $\\theta = 0.3$ with $n=3$ qubits

---

[[03 - Working Principle of QPE|← Previous: Working Principle]] | [[00 - QPE Study Guide Home|Study Guide]] | [[05 - Applications|Next: Applications →]]
