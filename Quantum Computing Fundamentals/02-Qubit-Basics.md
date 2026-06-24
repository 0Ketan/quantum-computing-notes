# 2. Qubit Basics

The qubit (quantum bit) is the fundamental unit of quantum information, analogous to the classical bit but with profound differences due to quantum mechanics.

## 2.1 Definition and State Space

A qubit is a two-level quantum system. Its state lives in a two-dimensional complex Hilbert space $\mathcal{H}_2 \cong \mathbb{C}^2$.

**General State**: 
$$|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$$
where $\alpha, \beta \in \mathbb{C}$ and $|\alpha|^2 + |\beta|^2 = 1$ (normalization condition).

**Computational Basis**: 
- $|0\rangle = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$ 
- $|1\rangle = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$

These form an orthonormal basis for $\mathbb{C}^2$.

## 2.2 Bloch Sphere Representation

Any pure qubit state can be visualized as a point on the surface of a unit sphere (Bloch sphere).

**Parametrization**:
$$|\psi\rangle = \cos\left(\frac{\theta}{2}\right)|0\rangle + e^{i\phi}\sin\left(\frac{\theta}{2}\right)|1\rangle$$
where:
- $\theta \in [0, \pi]$: polar angle from $|0\rangle$ axis
- $\phi \in [0, 2\pi)$: azimuthal angle from $|+\rangle$ axis in xy-plane

**Cartesian Coordinates** on Bloch sphere:
- $x = \sin\theta\cos\phi$
- $y = \sin\theta\sin\phi$ 
- $z = \cos\theta$

**Expectation Values** of Pauli operators:
- $\langle X \rangle = \langle\psi|X|\psi\rangle = \sin\theta\cos\phi$
- $\langle Y \rangle = \langle\psi|Y|\psi\rangle = \sin\theta\sin\phi$  
- $\langle Z \rangle = \langle\psi|Z|\psi\rangle = \cos\theta$

Thus the Bloch vector is $\vec{r} = (\langle X \rangle, \langle Y \rangle, \langle Z \rangle)$.

## 2.3 Special States

**Computational Basis States**:
- $|0\rangle$: $\theta = 0$, arbitrary $\phi$ (North pole)
- $|1\rangle$: $\theta = \pi$, arbitrary $\phi$ (South pole)

**Superposition States** (equator, $\theta = \pi/2$):
- $|+\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$: $\phi = 0$ (+x axis)
- $|-\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}}$: $\phi = \pi$ (-x axis)  
- $|+i\rangle = \frac{|0\rangle + i|1\rangle}{\sqrt{2}}$: $\phi = \pi/2$ (+y axis)
- $|-i\rangle = \frac{|0\rangle - i|1\rangle}{\sqrt{2}}$: $\phi = 3\pi/2$ (-y axis)

## 2.4 Density Matrix Representation

For pure states: $\rho = |\psi\rangle\langle\psi|$

**General Form** for qubit:
$$\rho = \frac{1}{2}(I + \vec{r}\cdot\vec{\sigma}) = \frac{1}{2}\begin{bmatrix} 1+z & x-iy \\ x+iy & 1-z \end{bmatrix}$$
where $\vec{r} = (x,y,z)$ is Bloch vector with $\|\vec{r}\| \leq 1$.

**Pure State**: $\|\vec{r}\| = 1$ (on surface of Bloch sphere)
**Mixed State**: $\|\vec{r}\| < 1$ (inside Bloch sphere)

**Maximally Mixed State**: 
$\rho = \frac{I}{2} = \begin{bmatrix} 1/2 & 0 \\ 0 & 1/2 \end{bmatrix}$ (center of Bloch sphere)
Represents complete ignorance about the state.

## 2.5 Measurement

**Projective Measurement** in computational basis:
- Probability of $|0\rangle$: $P(0) = |\langle 0|\psi\rangle|^2 = |\alpha|^2$
- Probability of $|1\rangle$: $P(1) = |\langle 1|\psi\rangle|^2 = |\beta|^2$
- Post-measurement state: 
  - If outcome $0$: $|0\rangle$
  - If outcome $1$: $|1\rangle$

**General Measurement** (POVM - Positive Operator-Valued Measure):
Set of positive operators $\{E_i\}$ with $\sum_i E_i = I$.
Probability of outcome $i$: $P(i) = \langle\psi|E_i|\psi\rangle$

For projective measurement, $E_i = |i\rangle\langle i|$ are projectors.

## 2.6 Time Evolution

**Schrödinger Equation** (in natural units $\hbar=1$):
$$i\frac{d}{dt}|\psi(t)\rangle = H(t)|\psi(t)\rangle$$
where $H(t)$ is Hamiltonian (Hermitian operator).

**Time-Independent Hamiltonian**:
$$|\psi(t)\rangle = e^{-iHt}|\psi(0)\rangle$$
where $U(t) = e^{-iHt}$ is unitary (time evolution operator).

**Example**: For $H = \frac{\omega}{2}Z$ (qubit in magnetic field along z):
$$|\psi(t)\rangle = e^{-i\omega t Z/2}|\psi(0)\rangle = \begin{bmatrix} e^{-i\omega t/2} & 0 \\ 0 & e^{i\omega t/2} \end{bmatrix}|\psi(0)\rangle$$
This causes precession around z-axis at frequency $\omega$ (Larmor precession).

## 2.7 Quantum vs Classical Bits

| Property | Classical Bit | Qubit |
|----------|---------------|--------|
| States | $\{0, 1\}$ | Continuum of $\alpha|0\rangle + \beta|1\rangle$ |
| Information | 1 bit (deterministic) | Infinite classical bits to specify $\alpha,\beta$ exactly |
| Measurement | Deterministic outcome | Probabilistic (Born rule) |
| State Change | Can copy/cloned | No-cloning theorem prevents exact copying |
| Correlation | Classical correlation | Can be entangled (non-classical correlations) |
| Manipulation | Boolean gates | Unitary gates (reversible) |

### Key Quantum Phenomena Exclusive to Qubits:

1. **Superposition**: Linear combination of basis states
2. **Entanglement**: Non-separable multi-qubit states  
3. **Interference**: Probability amplitudes can cancel/add
4. **No-Cloning**: Unknown quantum state cannot be copied perfectly
5. **Measurement Disturbance**: Measurement generally alters state

## Practice Problems

**Problem 2.1**: Express $|+\rangle$ and $|-\rangle$ in terms of $|0\rangle$ and $|1\rangle$, and find their Bloch sphere coordinates.

**Problem 2.2**: What is the Bloch vector for state $|\psi\rangle = \frac{1}{\sqrt{2}}(|0\rangle + i|1\rangle)$?

**Problem 2.3**: A qubit is in state $|\psi\rangle = \cos(\theta/2)|0\rangle + e^{i\phi}\sin(\theta/2)|1\rangle$. Calculate $\langle X \rangle$, $\langle Y \rangle$, and $\langle Z \rangle$.

**Problem 2.4**: Show that for any pure qubit state, $\langle X \rangle^2 + \langle Y \rangle^2 + \langle Z \rangle^2 = 1$.

**Problem 2.5**: If a qubit is measured in the $|+\rangle,|-\rangle$ basis and yields $|+\rangle$ with probability 3/4, what are possible states consistent with this?

**Problem 2.6**: A qubit starts in $|0\rangle$ and evolves under $H = \frac{\omega}{2}X$ for time $t$. Find the state at time $t$.

**Problem 2.7**: What is the density matrix for the maximally mixed state of a qubit? What is its Bloch vector?

**Problem 2.8**: Two qubits are in state $|\psi\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$. If the first qubit is measured and yields $|0\rangle$, what is the state of the second qubit?

## Solutions

**Solution 2.1**: 
$|+\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}} \Rightarrow \theta = \pi/2, \phi = 0 \Rightarrow (x,y,z) = (1,0,0)$
$|-\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}} \Rightarrow \theta = \pi/2, \phi = \pi \Rightarrow (x,y,z) = (-1,0,0)$

**Solution 2.2**: 
$|\psi\rangle = \frac{|0\rangle + i|1\rangle}{\sqrt{2}} \Rightarrow \theta = \pi/2, \phi = \pi/2 \Rightarrow (x,y,z) = (0,1,0)$

**Solution 2.3**: 
$\langle X \rangle = \sin\theta\cos\phi$
$\langle Y \rangle = \sin\theta\sin\phi$  
$\langle Z \rangle = \cos\theta$

**Solution 2.4**: 
$\langle X \rangle^2 + \langle Y \rangle^2 + \langle Z \rangle^2 = \sin^2\theta(\cos^2\phi+\sin^2\phi) + \cos^2\theta = \sin^2\theta + \cos^2\theta = 1$

**Solution 2.5**: 
$P(+) = |\langle +|\psi\rangle|^2 = \frac{3}{4}$
Let $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$
Then $|\langle +|\psi\rangle|^2 = \left|\frac{\alpha+\beta}{\sqrt{2}}\right|^2 = \frac{|\alpha+\beta|^2}{2} = \frac{3}{4}$
With $|\alpha|^2 + |\beta|^2 = 1$, solutions include $\alpha = \sqrt{3/4}, \beta = \sqrt{1/4}$ giving $|\psi\rangle = \sqrt{3/4}|0\rangle + \sqrt{1/4}|1\rangle$

**Solution 2.6**: 
$U(t) = e^{-i\omega t X/2} = \cos(\omega t/2)I - i\sin(\omega t/2)X$
$|\psi(t)\rangle = U(t)|0\rangle = \cos(\omega t/2)|0\rangle - i\sin(\omega t/2)|1\rangle$

**Solution 2.7**: 
$\rho = I/2 = \begin{bmatrix} 1/2 & 0 \\ 0 & 1/2 \end{bmatrix}$, Bloch vector $\vec{r} = (0,0,0)$

**Solution 2.8**: 
If first qubit measured as $|0\rangle$, state collapses to $|0\rangle\langle 0|\otimes I$ applied to $|\psi\rangle$, giving $|00\rangle$ (normalized). So second qubit is definitely $|0\rangle$.

---