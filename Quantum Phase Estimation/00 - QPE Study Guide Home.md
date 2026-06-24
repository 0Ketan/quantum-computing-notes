# 🔬 Quantum Phase Estimation (QPE) — Complete Study Guide

> **Your comprehensive learning resource for mastering QPE**
> Created for: Research Group Presentation | June 2026

---

## 📋 Study Roadmap

This guide is organized into **8 modules** that build on each other:

| Module | Topic | Prerequisites |
|--------|-------|---------------|
| **01** | [[01 - Introduction to QPE\|Introduction to QPE]] | None |
| **02** | [[02 - Fundamental Concepts\|Fundamental Concepts]] | Module 01 |
| **03** | [[03 - Working Principle of QPE\|Working Principle of QPE]] | Module 02 |
| **04** | [[04 - Mathematical Derivations\|Mathematical Derivations]] | Module 03 |
| **05** | [[05 - Applications\|Applications of QPE]] | Module 03 |
| **06** | [[06 - Advantages Challenges Future\|Advantages, Challenges & Future]] | All above |
| **07** | [[07 - QPE Code Examples\|QPE Code Examples (Qiskit)]] | Module 03 |
| **08** | [[08 - Practice Problems\|Practice Problems & Study Guide]] | All above |

---

## 🎯 Learning Objectives

By the end of this study, you should be able to:

- ✅ Explain **what QPE is** and why it matters in quantum computing
- ✅ Describe **qubits, superposition, unitary operators, and eigenstates**
- ✅ Understand **phase kickback** — the core mechanism behind QPE
- ✅ Walk through the **QPE circuit step by step**
- ✅ Derive the **mathematical framework** behind QPE
- ✅ Code QPE in **Qiskit** from scratch
- ✅ Explain **Shor's algorithm**, **quantum chemistry**, and **materials science** applications
- ✅ Discuss **current challenges** and **future prospects**

---

## 📚 Recommended Study Order

```
Week 1: Modules 01 → 02 → 03 (Theory Foundation)
Week 2: Module 04 (Deep Math) → Module 07 (Code Practice)
Week 3: Modules 05 → 06 (Applications & Future)  
Week 4: Module 08 (Practice Problems & Review)
```

---

## 🛠️ Tools at Your Disposal

| Tool | Purpose |
|------|---------|
| [[07 - QPE Code Examples\|Qiskit Notebook]] | Run and modify QPE circuits |
| [[04 - Mathematical Derivations\|Math Derivations]] | All formulas with step-by-step derivations |
| [[08 - Practice Problems\|Practice Problems]] | Test your understanding |
| [[Diagrams/]] | Visual circuit diagrams |
| **NotebookLM** | Audio overviews & infographics |

---

## ⚡ Quick Reference: The QPE Circuit

![[Diagrams/05_qpe_3ctrl_compact.png]]

```
  ╭─────────────────╮     ╭───────────────────╮
  │ Phase Encoding   │     │ Inverse QFT       │
  │ (Hadamard + CU)  │     │ (Read the phase)  │
  ╰─────────────────╯     ╰───────────────────╯
```

---

## 📖 Suggested External Resources

- 🔗 Nielsen & Chuang — *Quantum Computation and Quantum Information* (Ch. 5)
- 🔗 IBM Quantum Learning — QPE module
- 🔗 Qiskit Textbook — Chapter on QPE
- 🔗 arXiv: Quantum Phase Estimation — A Practical Guide

---

> *"Quantum Phase Estimation is to quantum computing what the Fourier transform is to classical computing — a fundamental building block that powers countless algorithms."*

[[01 - Introduction to QPE|→ Start with Module 01: Introduction to QPE]]
