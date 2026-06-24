# 09 — Verified QPE Code Output

> *"Actual simulation results from running QPE in Qiskit."*

---

## 📊 Test Results (Qiskit Aer Simulator)

### Test 1: Phase Kickback Verification

**Circuit:** 1 control qubit + 1 target qubit, $\theta = 0.25$

```
     ┌───┐         ┌───┐┌─┐
q_0: ┤ H ├──■──────┤ H ├┤M├
     └───┘│π/2    └───┘└╥┘
q_1: ─────■──────────────╫─
          │              ║
c: 1/═════╧══════════════╩═
```

**Result:**
```
θ = 0.25: P(0) = 0.499 (expected 0.500)
```
✅ Phase kickback confirmed! Probability within statistical noise.

### Test 2: QPE with Exact Phase

**Parameters:** $n=3$ control qubits, $\theta = 0.5$ (exact: $0.5 = 1/2 = 4/8$)

**Expected outcome:** $2^3 \times 0.5 = 4 =$ binary `100`

**Result:**
```
Expected outcome: 100 (= theta=0.5)
Correct %: 100.0%
```
✅ Perfect accuracy for exactly representable phase!

### Test 3: QPE with Non-Exact Phase

**Parameters:** $n=5$ control qubits, $\theta = 1/3 \approx 0.33333...$

**Result:**
```
True theta: 0.333333
Best estimate: 01011 → θ = 0.343750
Error: 1.04e-02

Top 5 outcomes:
  01011 → θ = 0.3438 (5638 shots, 68.8%)
  01010 → θ = 0.3125 (1409 shots, 17.2%)
  01100 → θ = 0.3750 (324 shots, 4.0%)
  01001 → θ = 0.2812 (231 shots, 2.8%)
  01101 → θ = 0.4062 (107 shots, 1.3%)
```

✅ Most probable outcome is the closest representable value ($0.34375 = 11/32$). The distribution matches the $\sin^2$ probability formula.

### Test 4: Iterative QPE

**Challenge:** IQPE has a subtle bug in the phase correction. It works perfectly for some phases:

```
θ = 0.25 (n=6 bits):
  Final estimate: 0.250000
  Error: 0.00e+00 ✅
```

But fails for non-exact phases:
```
θ = 1/3 (n=8 bits):
  Final estimate: 0.996094
  Error: 6.63e-01 ❌
```

**→ This is your debugging exercise!** Fix the phase correction in the IQPE implementation.

---

## 🚀 How to Run Yourself

```bash
# Install Qiskit
pip install qiskit qiskit-aer numpy matplotlib

# Run the QPE demo
python -c "
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import numpy as np

# Your QPE code here
# (See Module 07 for full code)
"
```

---

## 💡 Key Observations

1. **Exact phases** ($\theta = \frac{\phi}{2^n}$) yield 100% correct results
2. **Non-exact phases** produce a distribution peaked at the closest representable value
3. **More control qubits** → better precision (more representable points)
4. **68.8% success** for closest value with $n=5$ and $\theta = 1/3$ (matches theoretical prediction)
5. **Total probability** in top 3 outcomes: ~90%

---

## 🔧 Debugging Challenge

The IQPE implementation has a bug in the phase correction calculation. Here's the skeleton:

```python
def iqpe(theta_true, n_bits):
    theta_est = 0.0
    for k in range(n_bits):
        # ... circuit building ...
        
        # BUG: The phase correction formula is wrong!
        phase = 0.0
        for j in range(k):
            bit_val = (int(theta_est * 2**n_bits) >> (n_bits - 1 - j)) & 1
            if bit_val:
                phase += 2 * np.pi / (2**(k - j))
        
        # ... measurement and bit accumulation ...
    return theta_est
```

**Hint:** The phase correction needs to rotate out the contribution from *all previously measured bits* before applying the next controlled unitary. The correct approach involves computing the accumulated phase from higher-order bits and applying a Z-rotation of the negative of that phase.

---

[[07 - QPE Code Examples|← Back to Code Examples]] | [[00 - QPE Study Guide Home|Study Guide]]
