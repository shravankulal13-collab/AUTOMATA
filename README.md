# Automata Theory and Computability (BIS503T) - Assignment

This repository contains the complete assignment solutions, C simulation programs, transition diagrams, JFLAP files, and documentation for **Automata Theory & Computability (BIS503T)**, Department of Information Science & Engineering.

All theoretical designs strictly follow the standard faculty notations:
- States: $q_0, q_1, q_2, \dots$
- Start state marked with left arrow $\rightarrow$ / **Start**
- Final state marked with double circle / $*$
- PDA bottom-of-stack symbol: $Z_0$
- Turing Machine blank symbol: $B$
- Instantaneous descriptions with turnstile $\vdash$

---

## Repository Structure

```
├── ATC_Assignment_BIS503T.docx   # Complete Word document (editable cover page)
├── ATC_Assignment_BIS503T.pdf    # Complete compiled PDF report
├── q1_atm_dfa.c                  # Q1: ATM PIN Verification DFA simulator in C
├── q2_regex_search.c             # Q2: Regex Search Engine & Benchmark in C
├── q3_order_pda.c                # Q3: Online Order Processing PDA simulator in C
├── q4_tm_0n1n0n.c                # Q4: Turing Machine 0^n 1^n 0^n simulator in C
├── order_pda.jff                 # Q3: JFLAP Pushdown Automaton file
├── tm_0n1n0n.jff                 # Q4: JFLAP Turing Machine file
├── q1_atm_dfa.png                # Q1: Faculty-style DFA state diagram
├── q3_order_pda.png              # Q3: Faculty-style PDA diagram with stack box
├── q4_tm_0n1n0n.png              # Q4: Faculty-style TM state diagram
├── generate_diagrams.py          # Script used to generate high-res diagram PNGs
├── create_assignment_docx.py     # Script used to generate .docx report
└── create_assignment_pdf.py      # Script used to generate .pdf report
```

---

## Compilation & Execution (C Language)

### 1. Compile all C programs
Using `gcc`:
```bash
gcc -O2 q1_atm_dfa.c -o q1_atm_dfa.exe
gcc -O2 q2_regex_search.c -o q2_regex_search.exe
gcc -O2 q3_order_pda.c -o q3_order_pda.exe
gcc -O2 q4_tm_0n1n0n.c -o q4_tm_0n1n0n.exe
```

### 2. Run the executables
```bash
./q1_atm_dfa.exe
./q2_regex_search.exe
./q3_order_pda.exe
./q4_tm_0n1n0n.exe
```

---

## JFLAP Verification
- **Q3 (PDA)**: Open JFLAP $\rightarrow$ File $\rightarrow$ Open `order_pda.jff`. Initial stack symbol is `Z` ($Z_0$). Acceptance is configured *by final state*.
- **Q4 (Turing Machine)**: Open JFLAP $\rightarrow$ File $\rightarrow$ Open `tm_0n1n0n.jff`. Run *Step* or *Fast Run* with inputs like `010`, `001100`, etc.
