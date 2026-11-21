import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_document():
    doc = docx.Document()

    # Page Margins: 0.8 inch
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    # Style definitions
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

    # ------------------ COVER PAGE ------------------
    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_dept = p_dept.add_run("DEPARTMENT OF INFORMATION SCIENCE & ENGINEERING\n")
    r_dept.font.size = Pt(14)
    r_dept.font.bold = True
    r_dept.font.color.rgb = RGBColor(0x0d, 0x47, 0xa1)

    r_inst = p_dept.add_run("Autonomous Institute Affiliated to VTU | Belagavi\n\n")
    r_inst.font.size = Pt(11)
    r_inst.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("LABORATORY / THEORY COURSE ASSIGNMENT\nODD SEMESTER 2026 - 2027\n\n")
    r_title.font.size = Pt(16)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x1a, 0x23, 0x7e)

    r_sub = p_title.add_run("COURSE: AUTOMATA THEORY AND COMPUTABILITY\n")
    r_sub.font.size = Pt(14)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(0x0d, 0x47, 0xa1)

    r_code = p_title.add_run("Course Code: BIS503T\n\n")
    r_code.font.size = Pt(12)
    r_code.font.bold = True

    # Student metadata table
    table = doc.add_table(rows=6, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    data = [
        ("Student Name", "[ Student Name ]"),
        ("University Seat Number (USN)", "[ 1DS22IS___ ]"),
        ("Semester / Section", "V Semester / [ Section A / B ]"),
        ("Course Faculty", "Dr. Rithesh Pakkala P. / Dr. Sudheer Shetty"),
        ("Maximum Marks", "40 Marks"),
        ("Date of Submission", "21 - 11 - 2026")
    ]

    for row_idx, (k, v) in enumerate(data):
        row = table.rows[row_idx]
        cell_k, cell_v = row.cells[0], row.cells[1]
        cell_k.width = Inches(2.6)
        cell_v.width = Inches(4.0)
        set_cell_background(cell_k, "F0F4F8")
        set_cell_background(cell_v, "FFFFFF")
        set_cell_margins(cell_k, 120, 120, 150, 150)
        set_cell_margins(cell_v, 120, 120, 150, 150)

        p0 = cell_k.paragraphs[0]
        r0 = p0.add_run(k)
        r0.font.bold = True
        r0.font.size = Pt(10.5)

        p1 = cell_v.paragraphs[0]
        r1 = p1.add_run(v)
        r1.font.size = Pt(10.5)

    doc.add_paragraph("\n\n")

    # Table of contents box
    p_toc_head = doc.add_paragraph()
    r_th = p_toc_head.add_run("TABLE OF CONTENTS")
    r_th.font.bold = True
    r_th.font.size = Pt(12)
    r_th.font.color.rgb = RGBColor(0x0d, 0x47, 0xa1)

    toc_items = [
        ("Question 1", "Automated ATM PIN Verification System - Deterministic Finite Automaton (DFA)", "Page 2"),
        ("Question 2", "Regex-Based Mini Search Engine with Efficiency Analysis (C Implementation)", "Page 6"),
        ("Question 3", "Online Order Processing System - Pushdown Automaton (PDA) & JFLAP", "Page 10"),
        ("Question 4", "String Pattern Recognition {0^n 1^n 0^n | n >= 1} - Turing Machine & JFLAP", "Page 15")
    ]

    toc_table = doc.add_table(rows=len(toc_items)+1, cols=3)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = toc_table.rows[0]
    hdr.cells[0].paragraphs[0].add_run("No.").font.bold = True
    hdr.cells[1].paragraphs[0].add_run("Assignment Question & Topic").font.bold = True
    hdr.cells[2].paragraphs[0].add_run("Section").font.bold = True
    hdr.cells[0].width = Inches(0.8)
    hdr.cells[1].width = Inches(4.8)
    hdr.cells[2].width = Inches(1.0)
    for c in hdr.cells:
        set_cell_background(c, "E1EBF5")
        set_cell_margins(c, 100, 100, 120, 120)

    for idx, (q, desc, pg) in enumerate(toc_items):
        r = toc_table.rows[idx+1]
        r.cells[0].width = Inches(0.8)
        r.cells[1].width = Inches(4.8)
        r.cells[2].width = Inches(1.0)
        for c in r.cells:
            set_cell_background(c, "FAFAFA" if idx%2==0 else "FFFFFF")
            set_cell_margins(c, 80, 80, 120, 120)
        r.cells[0].paragraphs[0].add_run(q).font.bold = True
        r.cells[1].paragraphs[0].add_run(desc)
        r.cells[2].paragraphs[0].add_run(pg)

    doc.add_page_break()

    # ------------------ QUESTION 1 ------------------
    h1 = doc.add_heading("Question 1: Automated ATM PIN Verification System (DFA)", level=1)
    h1.style.font.color.rgb = RGBColor(0x0d, 0x47, 0xa1)

    doc.add_heading("1. Problem Statement", level=2)
    p = doc.add_paragraph(
        "An automated teller machine (ATM) requires a customer to enter a four-digit personal identification "
        "number (PIN). If the entered PIN matches the predefined PIN, access is granted. Otherwise, the customer "
        "may re-try, up to a maximum of three attempts. If the third attempt fails, access is permanently blocked.\n"
        "(a) Design a Deterministic Finite Automaton (DFA) for this verification process.\n"
        "(b) Simulate the machine for three representative test scenarios.\n"
        "(c) Implement the DFA simulation in C language.\n"
        "(d) Explain how finite automata help in designing secure authentication systems."
    )

    doc.add_heading("2. Design (Part a) - Faculty-Style Notation", level=2)
    doc.add_paragraph(
        "Design a DFA to accept valid authentication sequences over the alphabet Σ = { C , W }.\n"
        "Here each complete 4-digit entry is abstracted as one input symbol:\n"
        "  • C = Correct 4-digit PIN entered\n"
        "  • W = Wrong 4-digit PIN entered\n\n"
        "The language of accepted authentication sequences is given by:\n"
        "L = { C , WC , WWC , CC , CW , WCW , ... }\n"
        "where accepted sequences represent access granted within at most three attempts."
    )

    p_states = doc.add_paragraph()
    p_states.add_run("State Definitions:\n").font.bold = True
    p_states.add_run(
        "  • q0 : Initial state (Start) — no wrong attempt entered yet.\n"
        "  • q1 : Exactly one wrong attempt entered.\n"
        "  • q2 : Exactly two wrong attempts entered.\n"
        "  • q3 : ACCESS GRANTED (Final accepting state) — reached upon entering correct PIN.\n"
        "  • q4 : CARD BLOCKED (Trap / dead state) — reached after three consecutive failed attempts."
    )

    # Insert Diagram
    if os.path.exists("q1_atm_dfa.png"):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture("q1_atm_dfa.png", width=Inches(6.2))
        p_cap = doc.add_paragraph("Figure 1.1: State Transition Diagram of the ATM PIN Verification DFA")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(10)
        p_cap.runs[0].font.size = Pt(9.5)
        p_cap.runs[0].font.italic = True

    doc.add_paragraph("∴ The DFA can be given as:")
    p_dfa_def = doc.add_paragraph()
    r = p_dfa_def.add_run("A = ( { q0, q1, q2, q3, q4 } , { C, W } , δ , q0 , { q3 } )")
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x0d, 0x47, 0xa1)

    doc.add_paragraph("where δ can be given as:")

    # Transition Table
    tbl_dfa = doc.add_table(rows=6, cols=3)
    tbl_dfa.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["δ", "C (Correct PIN)", "W (Wrong PIN)"]
    for i, h in enumerate(headers):
        cell = tbl_dfa.rows[0].cells[i]
        cell.paragraphs[0].add_run(h).font.bold = True
        set_cell_background(cell, "E1EBF5")
        set_cell_margins(cell, 80, 80, 120, 120)

    rows_data = [
        ("→ q0", "q3", "q1"),
        ("   q1", "q3", "q2"),
        ("   q2", "q3", "q4"),
        (" * q3", "q3", "q3"),
        ("   q4", "q4", "q4")
    ]
    for row_idx, r_vals in enumerate(rows_data):
        row = tbl_dfa.rows[row_idx + 1]
        for col_idx, val in enumerate(r_vals):
            c = row.cells[col_idx]
            run = c.paragraphs[0].add_run(val)
            run.font.name = "Consolas"
            set_cell_background(c, "FAFAFA" if row_idx % 2 == 0 else "FFFFFF")
            set_cell_margins(c, 70, 70, 120, 120)

    doc.add_paragraph(
        "\nNotation Note: In the transition table, '→' denotes the Start state (q0) and '*' denotes the "
        "Final accepting state (q3). State q4 is an absorbing trap state: once entered, no subsequent input "
        "symbol can transition the machine away from q4.\n"
        "Remark on Digit-Level Machine: If the ATM reads raw decimal digits {0,1,...,9} for a fixed 4-digit PIN "
        "(e.g., 1234), the state space expands to 23 states: A1_0..A1_3, W1_1..W1_3, A2_0..A2_3, W2_1..W2_3, "
        "A3_0..A3_3, W3_1..W3_3, GRANTED, and BLOCKED. The 5-state machine above represents the precise attempt-level "
        "control automaton prescribed in faculty class notes."
    )

    doc.add_heading("3. Simulation (Part b) - Faculty State Sequence Format", level=2)
    doc.add_paragraph(
        "Simulation of the DFA on representative input sequences using the extended transition function δ^:\n\n"
        "1. Scenario 1 (Correct PIN on First Attempt):\n"
        "   Input: C\n"
        "   State Path:  q0 --(C)--> q3\n"
        "   Verdict: ACCEPTED => ACCESS GRANTED (Authentication successful on attempt 1).\n\n"
        "2. Scenario 2 (Wrong PIN, then Correct PIN on Second Attempt):\n"
        "   Input: WC\n"
        "   State Path:  q0 --(W)--> q1 --(C)--> q3\n"
        "   Verdict: ACCEPTED => ACCESS GRANTED (Authentication successful on attempt 2).\n\n"
        "3. Scenario 3 (Three Consecutive Wrong Attempts):\n"
        "   Input: WWW\n"
        "   State Path:  q0 --(W)--> q1 --(W)--> q2 --(W)--> q4\n"
        "   Verdict: REJECTED => CARD BLOCKED (Trap state q4 entered; maximum retries exceeded).\n\n"
        "4. Additional Scenario A (Correct PIN on Third Attempt):\n"
        "   Input: WWC\n"
        "   State Path:  q0 --(W)--> q1 --(W)--> q2 --(C)--> q3\n"
        "   Verdict: ACCEPTED => ACCESS GRANTED (Authentication successful on attempt 3).\n\n"
        "5. Additional Scenario B (Attempt Entered After Card Blocked):\n"
        "   Input: WWWC\n"
        "   State Path:  q0 --(W)--> q1 --(W)--> q2 --(W)--> q4 --(C)--> q4\n"
        "   Verdict: REJECTED => CARD BLOCKED (q4 self-loops; input C is ignored in trap state)."
    )

    doc.add_heading("4. Programming Code in C (Part c)", level=2)
    p_code = doc.add_paragraph()
    r_code = p_code.add_run(
        "/*\n"
        " * Course: Automata Theory and Computability (BIS503T)\n"
        " * Question 1: Automated ATM PIN Verification System using DFA\n"
        " * Faculty Notation: States q0, q1, q2, q3, q4 | Alphabet: Sigma = { C, W }\n"
        " */\n"
        "#include <stdio.h>\n"
        "#include <string.h>\n\n"
        "#define NUM_STATES 5\n"
        "#define NUM_SYMBOLS 2\n\n"
        "const char *state_names[NUM_STATES] = {\"q0\", \"q1\", \"q2\", \"q3\", \"q4\"};\n\n"
        "// delta[state][symbol]: 0 = 'C' (Correct), 1 = 'W' (Wrong)\n"
        "int delta[NUM_STATES][NUM_SYMBOLS] = {\n"
        "    {3, 1}, // -> q0: on C -> q3, on W -> q1\n"
        "    {3, 2}, //    q1: on C -> q3, on W -> q2\n"
        "    {3, 4}, //    q2: on C -> q3, on W -> q4\n"
        "    {3, 3}, //  * q3: on C -> q3, on W -> q3 (ACCESS GRANTED)\n"
        "    {4, 4}  //    q4: on C -> q4, on W -> q4 (CARD BLOCKED trap)\n"
        "};\n\n"
        "int map_symbol(char ch) {\n"
        "    if (ch == 'C' || ch == 'c') return 0;\n"
        "    if (ch == 'W' || ch == 'w') return 1;\n"
        "    return -1;\n"
        "}\n\n"
        "int simulate_dfa(const char *input, const char *scenario_name) {\n"
        "    int current_state = 0; // Start at q0\n"
        "    printf(\"----------------------------------------------------\\n\");\n"
        "    printf(\"Test Case: %s\\nInput Sequence: %s\\nState Transition Path:\\n  %s\",\n"
        "           scenario_name, input, state_names[current_state]);\n\n"
        "    for (int i = 0; input[i] != '\\0'; i++) {\n"
        "        int sym = map_symbol(input[i]);\n"
        "        if (sym == -1) {\n"
        "            printf(\"\\n[ERROR] Invalid symbol '%c'. Expected 'C' or 'W'.\\n\", input[i]);\n"
        "            return -1;\n"
        "        }\n"
        "        current_state = delta[current_state][sym];\n"
        "        printf(\" --(%c)--> %s\", input[i], state_names[current_state]);\n"
        "    }\n"
        "    printf(\"\\nFinal State: %s\\n\", state_names[current_state]);\n"
        "    if (current_state == 3) {\n"
        "        printf(\"Result: ACCEPTED => ACCESS GRANTED\\n\");\n"
        "        return 1;\n"
        "    } else if (current_state == 4) {\n"
        "        printf(\"Result: REJECTED => CARD BLOCKED (3 failed attempts)\\n\");\n"
        "        return 0;\n"
        "    } else {\n"
        "        printf(\"Result: INCOMPLETE => Waiting for further attempts\\n\");\n"
        "        return 0;\n"
        "    }\n"
        "}\n"
    )
    r_code.font.name = "Consolas"
    r_code.font.size = Pt(8.5)

    doc.add_heading("5. Execution Output & Verification Screenshots", level=2)
    doc.add_paragraph("Console output of the compiled C program (q1_atm_dfa.exe):")
    p_out = doc.add_paragraph()
    r_out = p_out.add_run(
        "====================================================\n"
        "         ATM PIN VERIFICATION DFA TABLE             \n"
        "====================================================\n"
        "   delta  |   C (Correct)   |   W (Wrong)          \n"
        "----------------------------------------------------\n"
        " -> q0    |      q3         |      q1              \n"
        "    q1    |      q3         |      q2              \n"
        "    q2    |      q3         |      q4              \n"
        "  * q3    |      q3         |      q3  (ACCESS GRANTED)\n"
        "    q4    |      q4         |      q4  (CARD BLOCKED)  \n"
        "====================================================\n\n"
        "----------------------------------------------------\n"
        "Test Case: Scenario 1: Correct PIN on First Attempt\n"
        "Input Sequence: C\n"
        "State Transition Path:\n"
        "  q0 --(C)--> q3\n"
        "Final State: q3\n"
        "Result: ACCEPTED => ACCESS GRANTED (Authentication Successful)\n"
        "----------------------------------------------------\n"
        "Test Case: Scenario 2: One Wrong Attempt, then Correct PIN\n"
        "Input Sequence: WC\n"
        "State Transition Path:\n"
        "  q0 --(W)--> q1 --(C)--> q3\n"
        "Final State: q3\n"
        "Result: ACCEPTED => ACCESS GRANTED (Authentication Successful)\n"
        "----------------------------------------------------\n"
        "Test Case: Scenario 3: Three Consecutive Wrong Attempts (Card Blocked)\n"
        "Input Sequence: WWW\n"
        "State Transition Path:\n"
        "  q0 --(W)--> q1 --(W)--> q2 --(W)--> q4\n"
        "Final State: q4\n"
        "Result: REJECTED => CARD BLOCKED (3 Failed Attempts Reached)\n"
        "----------------------------------------------------\n"
        "Test Case: Scenario 4: Two Wrong Attempts, Correct on Third Attempt\n"
        "Input Sequence: WWC\n"
        "State Transition Path:\n"
        "  q0 --(W)--> q1 --(W)--> q2 --(C)--> q3\n"
        "Final State: q3\n"
        "Result: ACCEPTED => ACCESS GRANTED (Authentication Successful)\n"
        "----------------------------------------------------\n"
        "Test Case: Scenario 5: Fourth Attempt Entered After Card is Blocked\n"
        "Input Sequence: WWWC\n"
        "State Transition Path:\n"
        "  q0 --(W)--> q1 --(W)--> q2 --(W)--> q4 --(C)--> q4\n"
        "Final State: q4\n"
        "Result: REJECTED => CARD BLOCKED (3 Failed Attempts Reached)\n"
        "----------------------------------------------------\n"
        "Test Case: Scenario 6: Access Granted, Subsequent Activity Absorbed\n"
        "Input Sequence: CW\n"
        "State Transition Path:\n"
        "  q0 --(C)--> q3 --(W)--> q3\n"
        "Final State: q3\n"
        "Result: ACCEPTED => ACCESS GRANTED (Authentication Successful)\n"
    )
    r_out.font.name = "Consolas"
    r_out.font.size = Pt(8.5)

    doc.add_heading("6. How Finite Automata Help in Secure Authentication Systems (Part d)", level=2)
    p_sec = doc.add_paragraph(
        "1. Deterministic and Fully Specified Behavior: A DFA defines exactly one valid transition for every pair "
        "of (state, symbol). There are no ambiguous, race-prone, or undefined edge cases that an attacker could exploit.\n\n"
        "2. State-Encoded Security Policies: The strict 3-attempt retry budget is hardcoded into the structural "
        "topology of states {q0, q1, q2, q4}. No external variable or software register that could be tampered with in memory "
        "is required.\n\n"
        "3. Absorbing Trap State (q4): Once the third failed attempt transitions the machine to q4, all subsequent inputs "
        "self-loop (δ(q4, C) = q4, δ(q4, W) = q4). The card cannot be unlocked through brute-force attempts without hardware administrative reset.\n\n"
        "4. Bounded Memory and Constant Time Complexity: A DFA requires O(1) space (only storing the current state index) "
        "and O(1) time per event (a single array lookup). This prevents side-channel timing attacks and is ideal for embedded hardware.\n\n"
        "5. Formal Verifiability: Because the state graph is finite, formal model-checking tools can mathematically prove "
        "that state q3 is strictly unreachable once state q4 is visited."
    )

    doc.add_page_break()

    # ------------------ QUESTION 2 ------------------
    h2 = doc.add_heading("Question 2: Building a Simple Regex-Based Search Engine", level=1)
    h2.style.font.color.rgb = RGBColor(0x0d, 0x47, 0xa1)

    doc.add_heading("1. Problem Statement", level=2)
    doc.add_paragraph(
        "Implement a mini search engine that accepts regular expressions and searches a collection of text documents "
        "for matching patterns. The implementation must comprise:\n"
        "  1. A User Interface (CLI/Console UI) with presets and custom search.\n"
        "  2. A backend regular expression matching engine.\n"
        "  3. An efficiency analysis section benchmarking different regular expression pattern categories."
    )

    doc.add_heading("2. Design & Architecture (C Implementation)", level=2)
    doc.add_paragraph(
        "The system is organized into four modular layers implemented in C:\n"
        "  • User Interface & Document Corpus: Manages documents (college circular, server logs, student contacts, "
        "lecture notes, and source code) and formats search results with highlighted match spans [>> MATCH <<].\n"
        "  • Regex Tokenizer & Parser: Decomposes the regular expression into branches (alternation '|') and atomic matchers.\n"
        "  • Matching Engine: Recursively simulates regular expression matching supporting literals, wildcards (.), "
        "character classes ([0-9], [a-z], [A-Z]), Kleene star (*), plus (+), and line anchors (^ and $).\n"
        "  • Performance Benchmark Module: Runs 10,000 iterations over the document corpus to evaluate microsecond execution "
        "timings across distinct regex patterns."
    )

    doc.add_heading("3. Programming Code in C", level=2)
    p_c2 = doc.add_paragraph()
    r_c2 = p_c2.add_run(
        "/*\n"
        " * Question 2: Regex-Based Mini Search Engine in C\n"
        " * Core Matching Engine & Benchmarking Module\n"
        " */\n"
        "#include <stdio.h>\n"
        "#include <string.h>\n"
        "#include <time.h>\n\n"
        "// Recursive matcher supporting literals, '.', character classes, and '*'\n"
        "static int match_here(const char *regexp, const char *text, int *match_len);\n\n"
        "static int char_matches(char pat_char, char text_char) {\n"
        "    if (pat_char == '.') return (text_char != '\\0');\n"
        "    return (pat_char == text_char);\n"
        "}\n\n"
        "int regex_search(const char *pattern, const char *text, int *out_start, int *out_len) {\n"
        "    char pat_copy[128];\n"
        "    strncpy(pat_copy, pattern, sizeof(pat_copy)-1);\n"
        "    pat_copy[sizeof(pat_copy)-1] = '\\0';\n"
        "    char *branch = strtok(pat_copy, \"|\"); // Alternation support\n"
        "    while (branch != NULL) {\n"
        "        int s = 0, l = 0;\n"
        "        if (search_single_branch(branch, text, &s, &l)) {\n"
        "            *out_start = s; *out_len = l;\n"
        "            return 1;\n"
        "        }\n"
        "        branch = strtok(NULL, \"|\");\n"
        "    }\n"
        "    return 0;\n"
        "}\n"
    )
    r_c2.font.name = "Consolas"
    r_c2.font.size = Pt(8.5)

    doc.add_heading("4. Execution Output (Search Demonstration)", level=2)
    p_c2_out = doc.add_paragraph()
    r_c2_out = p_c2_out.add_run(
        "=================================================================\n"
        " Search Results for Pattern: \"ERROR|WARN\"\n"
        "=================================================================\n"
        "[Document: server_log.txt]\n"
        "  Line 2: 2026-11-20 09:15:47  [>> WARN <<]   user=unknown  action=login status=401\n"
        "  Line 3: 2026-11-20 10:02:11  [>> ERROR <<]  user=admin    action=db_query status=500\n"
        "  Line 4: 2026-11-20 11:30:00  [>> ERROR <<]  user=guest    action=upload status=403\n"
        " Summary: 3 match(es) found across 1 document(s).\n\n"
        "=================================================================\n"
        " Search Results for Pattern: \"[0-9]+-[0-9]+-[0-9]+\"\n"
        "=================================================================\n"
        "[Document: college_circular.txt]\n"
        "  Line 1: Circular No 45/2026 Date  [>> 12-08-2 <<] 026\n"
        "  Line 2: IA-1 exam begins on  [>> 15-09-2 <<] 026 for 5th semester students.\n"
        "  Line 4: Final assignment submission deadline is  [>> 21-11-2 <<] 026.\n"
        "[Document: server_log.txt]\n"
        "  Line 1:  [>> 2026-11-2 <<] 0 09:15:22 INFO  user=student1 action=login status=200\n"
        "  Line 2:  [>> 2026-11-2 <<] 0 09:15:47 WARN  user=unknown  action=login status=401\n"
        "  Line 3:  [>> 2026-11-2 <<] 0 10:02:11 ERROR user=admin    action=db_query status=500\n"
        " Summary: 8 match(es) found across 2 document(s).\n\n"
        "=================================================================\n"
        " Search Results for Pattern: \"college.edu\"\n"
        "=================================================================\n"
        "[Document: college_circular.txt]\n"
        "  Line 3: Contact hod.ise@ [>> college.edu <<]  or office@college.edu for queries.\n"
        "[Document: student_contacts.txt]\n"
        "  Line 4: Name: Dr. Pakkala  Faculty ISE     Email: rithesh.p@ [>> college.edu <<] \n"
        " Summary: 2 match(es) found across 2 document(s).\n"
    )
    r_c2_out.font.name = "Consolas"
    r_c2_out.font.size = Pt(8.5)

    doc.add_heading("5. Efficiency Analysis of Different Regex Patterns", level=2)
    doc.add_paragraph("Benchmarking results over 10,000 passes across the document repository:")

    tbl_bench = doc.add_table(rows=10, cols=4)
    tbl_bench.alignment = WD_TABLE_ALIGNMENT.CENTER
    b_heads = ["Regex Pattern", "Pattern Category", "Execution Time (ms)", "Hits / Pass"]
    for i, h in enumerate(b_heads):
        cell = tbl_bench.rows[0].cells[i]
        cell.paragraphs[0].add_run(h).font.bold = True
        set_cell_background(cell, "E1EBF5")
        set_cell_margins(cell, 80, 80, 100, 100)

    b_data = [
        ("ERROR", "Plain Literal", "119.00 ms", "2"),
        ("^2026", "Start-Anchored Literal", "25.00 ms", "5"),
        ("status=200$", "End-Anchored Literal", "134.00 ms", "2"),
        ("ERROR|WARN", "Binary Alternation", "206.00 ms", "3"),
        ("ERROR|WARN|INFO", "Ternary Alternation", "288.00 ms", "5"),
        ("[0-9]+-[0-9]+-[0-9]+", "Character Class + Quantifier", "243.00 ms", "8"),
        ("d.t.", "Wildcard Sequence", "126.00 ms", "0"),
        ("[a-z]*college", "Kleene Star Prefix", "674.00 ms", "2"),
        ("TODO|FIXME", "Code Tag Alternation", "215.00 ms", "2")
    ]
    for r_idx, row_vals in enumerate(b_data):
        row = tbl_bench.rows[r_idx + 1]
        for c_idx, val in enumerate(row_vals):
            c = row.cells[c_idx]
            run = c.paragraphs[0].add_run(val)
            if c_idx == 0 or c_idx == 2:
                run.font.name = "Consolas"
            set_cell_background(c, "FAFAFA" if r_idx % 2 == 0 else "FFFFFF")
            set_cell_margins(c, 70, 70, 100, 100)

    doc.add_paragraph(
        "\nTheoretical Analysis & Findings:\n"
        "1. Anchored Patterns are Fastest (25.00 ms): Anchoring at line start ('^') eliminates the need to scan "
        "subsequent character positions across the line; if index 0 does not match, the entire line is pruned immediately.\n"
        "2. Cost of Alternation Grows Linearly (206 ms -> 288 ms): Each alternation branch '|' is evaluated "
        "sequentially until a match is confirmed, multiplying the scanning effort across candidates.\n"
        "3. Kleene Star Prefix Backtracking Overhead (674.00 ms): Patterns like '[a-z]*college' suffer from "
        "backtracking because the greedy star initially matches as many lowercase characters as possible, then rewinds "
        "character-by-character to locate the literal suffix 'college'.\n"
        "4. Practical Recommendation: Use explicit prefixes and start anchors where feasible; avoid unanchored "
        "leading wildcards (.*) which trigger unnecessary worst-case quadratic comparisons."
    )

    doc.add_page_break()

    # ------------------ QUESTION 3 ------------------
    h3 = doc.add_heading("Question 3: Online Order Processing System (PDA)", level=1)
    h3.style.font.color.rgb = RGBColor(0x0d, 0x47, 0xa1)

    doc.add_heading("1. Problem Statement", level=2)
    doc.add_paragraph(
        "In an e-commerce transaction workflow, every order must be placed before its payment confirmation, "
        "and every payment confirmation must correspond to a previously placed unpaid order.\n"
        "(a) Design a Pushdown Automaton (PDA) to recognize valid sequences of orders and payments.\n"
        "(b) Explain how the stack maintains pending-order information.\n"
        "(c) Simulate the PDA on valid and invalid sequences using Instantaneous Descriptions (IDs).\n"
        "(d) Implement the design in JFLAP (using file order_pda.jff).\n"
        "(e) Discuss the significance of PDAs for stack-based workflows."
    )

    doc.add_heading("2. Design (Part a) - Faculty-Style Notation", level=2)
    doc.add_paragraph(
        "Design a PDA for the language L over alphabet Σ = { o, p } where:\n"
        "  • o = order placed\n"
        "  • p = payment confirmed\n\n"
        "A sequence w is valid if and only if in every prefix the number of payments does not exceed orders, "
        "and the total number of orders equals payments (the Dyck language of balanced parentheses):\n"
        "L = { w ∈ { o, p }* | every prefix has #o ≥ #p and #o(w) = #p(w) }\n"
        "Sample strings: L = { ε, op, oopp, opop, ooppop, ... }    Sample string: w = oopp\n\n"
        "The required PDA P is given by:"
    )

    p_pda_def = doc.add_paragraph()
    r_pda = p_pda_def.add_run("P = ( { q0, q1 } , { o, p } , { O, Z0 } , δ , q0 , Z0 , { q1 } )")
    r_pda.font.bold = True
    r_pda.font.color.rgb = RGBColor(0x0d, 0x47, 0xa1)

    doc.add_paragraph(
        "Acceptance is by FINAL STATE (state q1). The bottom-of-stack marker is Z0.\n"
        "where δ is given by:"
    )

    p_delta_pda = doc.add_paragraph()
    r_rules_pda = p_delta_pda.add_run(
        "δ( q0 , o , Z0 ) = { ( q0 , OZ0 ) }\n"
        "δ( q0 , o , O  ) = { ( q0 , OO ) }\n"
        "δ( q0 , p , O  ) = { ( q0 , ε ) }\n"
        "δ( q0 , ε , Z0 ) = { ( q1 , Z0 ) }"
    )
    r_rules_pda.font.name = "Consolas"
    r_rules_pda.font.bold = True

    # Insert PDA Diagram
    if os.path.exists("q3_order_pda.png"):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture("q3_order_pda.png", width=Inches(5.8))
        p_cap = doc.add_paragraph("Figure 3.1: Transition Diagram of the Order Processing PDA with Stack Memory Box")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(10)
        p_cap.runs[0].font.size = Pt(9.5)
        p_cap.runs[0].font.italic = True

    doc.add_heading("3. How the Stack Maintains Pending-Order Information (Part b)", level=2)
    doc.add_paragraph(
        "1. Dynamic Stack Height: The stack height above Z0 is always equal to (#orders placed − #payments confirmed), "
        "representing the exact count of currently outstanding, unpaid orders.\n\n"
        "2. Pushing on Order Placement ('o'): When symbol 'o' arrives, if stack top is Z0 or O, another 'O' is pushed "
        "onto the stack (δ(q0, o, Z0) = (q0, OZ0); δ(q0, o, O) = (q0, OO)).\n\n"
        "3. Popping on Payment ('p'): When payment 'p' occurs, one pending order 'O' is popped (δ(q0, p, O) = (q0, ε)). "
        "If a payment is attempted when the top of stack is Z0 (no pending orders), no transition exists; the machine immediately halts and rejects.\n\n"
        "4. Verification at End of Stream (ε-move): Reaching the accepting final state q1 requires the transition "
        "δ(q0, ε, Z0) = (q1, Z0). This can ONLY occur if all orders have been matched and paid, leaving Z0 exposed at the top. "
        "If any order remains unpaid, 'O' remains above Z0, preventing entry into q1 and correctly rejecting the string."
    )

    doc.add_heading("4. Simulation Using Instantaneous Descriptions (Part c)", level=2)
    doc.add_paragraph(
        "Instantaneous descriptions are written in the faculty's notation (state, remaining input, stack) "
        "with top of stack on the LEFT, using turnstile ⊢:\n\n"
        "Valid Case 1 (Single Order & Payment): w = op\n"
        "  ( q0 , op , Z0 ) ⊢ ( q0 , p , OZ0 ) ⊢ ( q0 , ε , Z0 ) ⊢ ( q1 , ε , Z0 )  => ACCEPTED\n\n"
        "Valid Case 2 (Nested Orders): w = oopp\n"
        "  ( q0 , oopp , Z0 ) ⊢ ( q0 , opp , OZ0 ) ⊢ ( q0 , pp , OOZ0 ) ⊢ ( q0 , p , OZ0 ) ⊢ ( q0 , ε , Z0 ) ⊢ ( q1 , ε , Z0 )  => ACCEPTED\n\n"
        "Valid Case 3 (Sequential Transactions): w = opop\n"
        "  ( q0 , opop , Z0 ) ⊢ ( q0 , pop , OZ0 ) ⊢ ( q0 , op , Z0 ) ⊢ ( q0 , p , OZ0 ) ⊢ ( q0 , ε , Z0 ) ⊢ ( q1 , ε , Z0 )  => ACCEPTED\n\n"
        "Valid Case 4 (Mixed Nested & Sequential): w = ooppop\n"
        "  ( q0 , ooppop , Z0 ) ⊢ ( q0 , oppop , OZ0 ) ⊢ ( q0 , ppop , OOZ0 ) ⊢ ( q0 , pop , OZ0 ) ⊢ ( q0 , op , Z0 ) ⊢ ( q0 , p , OZ0 ) ⊢ ( q0 , ε , Z0 ) ⊢ ( q1 , ε , Z0 )  => ACCEPTED\n\n"
        "Valid Case 5 (Empty Transaction Stream): w = ε\n"
        "  ( q0 , ε , Z0 ) ⊢ ( q1 , ε , Z0 )  => ACCEPTED\n\n"
        "Invalid Case 1 (Payment Before Order): w = po\n"
        "  ( q0 , po , Z0 ) -> Stuck! No rule for δ(q0, p, Z0)  => REJECTED\n\n"
        "Invalid Case 2 (Unpaid Order Remaining): w = oop\n"
        "  ( q0 , oop , Z0 ) ⊢ ( q0 , op , OZ0 ) ⊢ ( q0 , p , OOZ0 ) ⊢ ( q0 , ε , OZ0 ) -> Stuck at q0; 'O' remains on stack  => REJECTED\n\n"
        "Invalid Case 3 (Surplus Payment): w = opp\n"
        "  ( q0 , opp , Z0 ) ⊢ ( q0 , pp , OZ0 ) ⊢ ( q0 , p , Z0 ) -> Stuck! No rule for δ(q0, p, Z0)  => REJECTED\n\n"
        "Invalid Case 4 (Surplus Payment Followed by Order): w = oppo\n"
        "  ( q0 , oppo , Z0 ) ⊢ ( q0 , ppo , OZ0 ) ⊢ ( q0 , po , Z0 ) -> Stuck! No rule for δ(q0, p, Z0)  => REJECTED"
    )

    doc.add_heading("5. Programming Code in C", level=2)
    p_c3 = doc.add_paragraph()
    r_c3 = p_c3.add_run(
        "/*\n"
        " * Question 3: Online Order Processing System using PDA in C\n"
        " * Implements exact faculty transitions & prints IDs with |-\n"
        " */\n"
        "#include <stdio.h>\n"
        "#include <string.h>\n"
        "#include <stdbool.h>\n\n"
        "typedef struct { char items[100]; int size; } PDAStack;\n\n"
        "bool simulate_pda(const char *input, const char *label) {\n"
        "    int state = 0; PDAStack stack; stack.items[0] = 'Z'; stack.items[1] = '\\0'; stack.size = 1;\n"
        "    int in_idx = 0, in_len = strlen(input);\n"
        "    printf(\"   ( q%d , %-8s , %s )\\n\", state, input[0]=='\\0'?\"epsilon\":input, stack.items);\n"
        "    while (in_idx < in_len) {\n"
        "        char ch = input[in_idx], top = stack.items[0];\n"
        "        if (state == 0 && ch == 'o' && top == 'Z') { stack_push(&stack, 'O'); in_idx++; }\n"
        "        else if (state == 0 && ch == 'o' && top == 'O') { stack_push(&stack, 'O'); in_idx++; }\n"
        "        else if (state == 0 && ch == 'p' && top == 'O') { stack_pop(&stack); in_idx++; }\n"
        "        else return false; // Machine stuck\n"
        "        printf(\" |- ( q%d , %-8s , %s )\\n\", state, (in_idx==in_len)?\"epsilon\":(input+in_idx), stack.items);\n"
        "    }\n"
        "    if (state == 0 && stack.items[0] == 'Z') {\n"
        "        state = 1; // Transition to final state q1 on epsilon\n"
        "        printf(\" |- ( q%d , epsilon  , %s )   [via delta(q0, epsilon, Z0) = (q1, Z0)]\\n\", state, stack.items);\n"
        "    }\n"
        "    return (state == 1);\n"
        "}\n"
    )
    r_c3.font.name = "Consolas"
    r_c3.font.size = Pt(8.5)

    doc.add_heading("6. Execution Output & Verification", level=2)
    p_c3_out = doc.add_paragraph()
    r_c3_out = p_c3_out.add_run(
        "=======================================================================\n"
        "Test Case: Valid 2: Nested Orders (Two orders, then both paid)\n"
        "Input String w = \"oopp\"\n"
        "Instantaneous Descriptions (IDs):\n"
        "   ( q0 , oopp     , Z0 )\n"
        " |- ( q0 , opp      , OZ0 )\n"
        " |- ( q0 , pp       , OOZ0 )\n"
        " |- ( q0 , p        , OZ0 )\n"
        " |- ( q0 , epsilon  , Z0 )\n"
        " |- ( q1 , epsilon  , Z0 )   [via delta( q0 , epsilon , Z0 ) = ( q1 , Z0 )]\n"
        "Verdict: ACCEPTED (Valid order-payment sequence; reaches final state q1)\n"
        "-----------------------------------------------------------------------\n"
        "Test Case: Invalid 1: Payment Attempted Before Any Order\n"
        "Input String w = \"po\"\n"
        "Instantaneous Descriptions (IDs):\n"
        "   ( q0 , po       , Z0 )\n"
        "Verdict: REJECTED (Invalid sequence: Machine stuck (no valid transition defined))\n"
        "-----------------------------------------------------------------------\n"
        "Test Case: Invalid 2: Unpaid Order Remaining (2 orders, 1 payment)\n"
        "Input String w = \"oop\"\n"
        "Instantaneous Descriptions (IDs):\n"
        "   ( q0 , oop      , Z0 )\n"
        " |- ( q0 , op       , OZ0 )\n"
        " |- ( q0 , p        , OOZ0 )\n"
        " |- ( q0 , epsilon  , OZ0 )\n"
        "Verdict: REJECTED (Invalid sequence: Orders left unpaid; stack contains O)\n"
        "=======================================================================\n"
        "EXHAUSTIVE VERIFICATION ON ALL STRINGS OVER {o, p} UP TO LENGTH 10:\n"
        "Tested 2047 strings: 2047 Passed, 0 Mismatches -> 100% VERIFIED!\n"
    )
    r_c3_out.font.name = "Consolas"
    r_c3_out.font.size = Pt(8.5)

    doc.add_heading("7. Implementation in JFLAP (Part d)", level=2)
    doc.add_paragraph(
        "The Pushdown Automaton was implemented and verified in JFLAP (saved as order_pda.jff):\n"
        "1. Open JFLAP -> Select 'Pushdown Automaton'.\n"
        "2. Create state q0 (Initial) and state q1 (Final).\n"
        "3. Configure transitions in JFLAP format (read, pop ; push) with initial stack symbol Z (representing Z0):\n"
        "   • On q0:  o , Z ; OZ\n"
        "   • On q0:  o , O ; OO\n"
        "   • On q0:  p , O ; λ\n"
        "   • q0 -> q1:  λ , Z ; Z\n"
        "4. In JFLAP Preferences, ensure Acceptance is configured as 'Accept by Final State'.\n"
        "5. Use 'Multiple Run' to verify all test strings simultaneously."
    )

    doc.add_heading("8. Significance of PDAs for Stack-Based Workflows (Part e)", level=2)
    doc.add_paragraph(
        "• Unbounded Nesting Support: Finite automata have fixed memory and cannot count arbitrarily high numbers "
        "of pending transactions. A PDA provides an unbounded stack memory, allowing arbitrary depths of pending orders.\n"
        "• LIFO Transaction Scoping: Stack memory naturally models Last-In-First-Out nesting patterns such as "
        "nested order lines, split shipments, hierarchical XML/JSON order payloads, and database savepoints/rollbacks.\n"
        "• Equivalence to Context-Free Grammars: The language L is generated by the CFG: S -> oSpS | ε, "
        "which forms the formal foundation of syntax checkers and business process workflow engines."
    )

    doc.add_page_break()

    # ------------------ QUESTION 4 ------------------
    h4 = doc.add_heading("Question 4: String Pattern Recognition (Turing Machine)", level=1)
    h4.style.font.color.rgb = RGBColor(0x0d, 0x47, 0xa1)

    doc.add_heading("1. Problem Statement", level=2)
    doc.add_paragraph(
        "In a data processing system, binary records are validated against the pattern:\n"
        "\"an equal number of zeros, ones, and zeros in three consecutive groups (at least one each)\".\n"
        "The language is formally defined as:\n"
        "  L = { 0^n 1^n 0^n | n ≥ 1 }\n"
        "Sample strings: 010, 001100, 000111000 ∈ L;  00110, 0101 ∉ L.\n"
        "(a) Design a single-tape Deterministic Turing Machine (TM) for this language.\n"
        "(b) Explain how the machine marks and matches symbols across the three groups.\n"
        "(c) Simulate the TM step-by-step for w = 001100 and analyze test cases.\n"
        "(d) Implement the machine in JFLAP (tm_0n1n0n.jff).\n"
        "(e) Explain why a Turing machine is required and its computational capability."
    )

    doc.add_heading("2. Design (Part a) - Faculty-Style Notation", level=2)
    doc.add_paragraph(
        "Design a Turing Machine to accept L = { 0^n 1^n 0^n | n ≥ 1 } with sample string w = 001100.\n\n"
        "The required Turing Machine M is given by:"
    )

    p_tm_def = doc.add_paragraph()
    r_tm = p_tm_def.add_run("M = ( { q0, q1, q2, q3, q4, q5 } , { 0, 1 } , { 0, 1, X, Y, Z, B } , δ , q0 , B , { q5 } )")
    r_tm.font.bold = True
    r_tm.font.color.rgb = RGBColor(0x0d, 0x47, 0xa1)

    doc.add_paragraph(
        "where Blank symbol = B, Start state = q0, Final state = { q5 }, and markers X, Y, Z represent marked "
        "0s of group 1, 1s of group 2, and 0s of group 3 respectively.\n"
        "The transition function δ is given one rule per line as δ( state , symbol ) = ( newstate , written symbol , direction ):"
    )

    p_tm_rules = doc.add_paragraph()
    r_rules_tm = p_tm_rules.add_run(
        "δ( q0 , 0 ) = ( q1 , X , R )        mark first 0 of group 1\n"
        "δ( q0 , Y ) = ( q4 , Y , R )        group 1 finished -> verify\n"
        "δ( q1 , 0 ) = ( q1 , 0 , R )\n"
        "δ( q1 , Y ) = ( q1 , Y , R )\n"
        "δ( q1 , 1 ) = ( q2 , Y , R )        mark first 1 of group 2\n"
        "δ( q2 , 1 ) = ( q2 , 1 , R )\n"
        "δ( q2 , Z ) = ( q2 , Z , R )\n"
        "δ( q2 , 0 ) = ( q3 , Z , L )        mark first 0 of group 3\n"
        "δ( q3 , 0 ) = ( q3 , 0 , L )\n"
        "δ( q3 , 1 ) = ( q3 , 1 , L )\n"
        "δ( q3 , Y ) = ( q3 , Y , L )\n"
        "δ( q3 , Z ) = ( q3 , Z , L )\n"
        "δ( q3 , X ) = ( q0 , X , R )        back at right-most X, start next round\n"
        "δ( q4 , Y ) = ( q4 , Y , R )\n"
        "δ( q4 , Z ) = ( q4 , Z , R )\n"
        "δ( q4 , B ) = ( q5 , B , R )        only marked symbols left -> ACCEPT"
    )
    r_rules_tm.font.name = "Consolas"
    r_rules_tm.font.bold = True

    # Insert TM Diagram
    if os.path.exists("q4_tm_0n1n0n.png"):
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture("q4_tm_0n1n0n.png", width=Inches(6.4))
        p_cap = doc.add_paragraph("Figure 4.1: Transition Diagram of the Turing Machine for L = { 0^n 1^n 0^n | n >= 1 }")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(10)
        p_cap.runs[0].font.size = Pt(9.5)
        p_cap.runs[0].font.italic = True

    doc.add_heading("3. How the Machine Marks and Matches the Three Groups (Part b)", level=2)
    doc.add_paragraph(
        "Each multi-state sweep corresponds to matching exactly one symbol across the three groups:\n"
        "  1. Group 1 Marking (q0 -> q1): State q0 finds the leftmost unmarked '0' and replaces it with 'X', moving Right to q1.\n"
        "  2. Group 2 Marking (q1 -> q2): State q1 skips over any remaining '0's and already-marked 'Y's until it finds "
        "the leftmost unmarked '1'. It replaces '1' with 'Y' and moves Right to q2.\n"
        "  3. Group 3 Marking (q2 -> q3): State q2 skips over remaining '1's and already-marked 'Z's until it reaches "
        "the leftmost unmarked '0' of group 3. It replaces '0' with 'Z' and transitions to q3, moving Left.\n"
        "  4. Leftward Rewind (q3 -> q0): State q3 moves Left over all 0s, 1s, Ys, and Zs until it hits the most recently "
        "written marker 'X'. It steps one cell Right into q0 to begin the next matching round.\n"
        "  5. Acceptance Verification (q0 -> q4 -> q5): When q0 sees 'Y' instead of '0', group 1 is completely exhausted. "
        "It switches to state q4, which scans Right ensuring no leftover unmarked '1's or '0's exist. Upon reading Blank 'B', "
        "it enters accepting state q5."
    )

    doc.add_heading("4. Tape Trace in Faculty Style (Part c)", level=2)
    doc.add_paragraph(
        "Complete step-by-step tape trace for sample string w = 001100 (faculty notation with tape contents on line, "
        "arrow ^ pointing to the tape head cell, and current state directly under the arrow):\n"
    )

    p_tm_tr = doc.add_paragraph()
    r_tm_tr = p_tm_tr.add_run(
        "Step  0 | Tape:  0  0  1  1  0  0  B \n"
        "         Head:  ^ \n"
        "         State: q0\n"
        "Step  1 | Tape:  X  0  1  1  0  0  B \n"
        "         Head:     ^ \n"
        "         State:    q1\n"
        "Step  2 | Tape:  X  0  1  1  0  0  B \n"
        "         Head:        ^ \n"
        "         State:       q1\n"
        "Step  3 | Tape:  X  0  Y  1  0  0  B \n"
        "         Head:           ^ \n"
        "         State:          q2\n"
        "Step  4 | Tape:  X  0  Y  1  0  0  B \n"
        "         Head:              ^ \n"
        "         State:             q2\n"
        "Step  5 | Tape:  X  0  Y  1  Z  0  B \n"
        "         Head:           ^ \n"
        "         State:          q3\n"
        "Step  6 | Tape:  X  0  Y  1  Z  0  B \n"
        "         Head:        ^ \n"
        "         State:       q3\n"
        "Step  7 | Tape:  X  0  Y  1  Z  0  B \n"
        "         Head:     ^ \n"
        "         State:    q3\n"
        "Step  8 | Tape:  X  0  Y  1  Z  0  B \n"
        "         Head:  ^ \n"
        "         State: q3\n"
        "Step  9 | Tape:  X  0  Y  1  Z  0  B \n"
        "         Head:     ^ \n"
        "         State:    q0  <-- Round 1 Completed: One 0, 1, 0 marked\n"
        "Step 10 | Tape:  X  X  Y  1  Z  0  B \n"
        "         Head:        ^ \n"
        "         State:       q1\n"
        "Step 11 | Tape:  X  X  Y  1  Z  0  B \n"
        "         Head:           ^ \n"
        "         State:          q1\n"
        "Step 12 | Tape:  X  X  Y  Y  Z  0  B \n"
        "         Head:              ^ \n"
        "         State:             q2\n"
        "Step 13 | Tape:  X  X  Y  Y  Z  0  B \n"
        "         Head:                 ^ \n"
        "         State:                q2\n"
        "Step 14 | Tape:  X  X  Y  Y  Z  Z  B \n"
        "         Head:              ^ \n"
        "         State:             q3\n"
        "Step 18 | Tape:  X  X  Y  Y  Z  Z  B \n"
        "         Head:        ^ \n"
        "         State:       q0  <-- Round 2 Completed\n"
        "Step 19 | Tape:  X  X  Y  Y  Z  Z  B \n"
        "         Head:           ^ \n"
        "         State:          q4  <-- Group 1 exhausted; scanning to verify\n"
        "Step 22 | Tape:  X  X  Y  Y  Z  Z  B \n"
        "         Head:                    ^ \n"
        "         State:                   q4\n"
        "Step 23 | Tape:  X  X  Y  Y  Z  Z  B  B \n"
        "         Head:                       ^ \n"
        "         State:                      q5  <-- ACCEPTED (Final State Reached)\n"
    )
    r_tm_tr.font.name = "Consolas"
    r_tm_tr.font.size = Pt(8.0)

    doc.add_paragraph(
        "Summary of Other Required Test Cases:\n"
        "  • w = 010 (n = 1): Accepted in 8 steps (010 -> X10 -> XY0 -> XYZ -> q5 accept).\n"
        "  • w = 000111000 (n = 3): Accepted in 46 steps across 3 rounds.\n"
        "  • w = 00110: Rejected after 13 steps. Round 2 attempts to find second '0' of group 3, but reads Blank 'B'; "
        "no move δ(q2, B) exists -> halts in non-final state q2.\n"
        "  • w = 0101: Rejected after 7 steps. Interleaved ordering violates group structure; state q4 encounters '1' "
        "where only Z or B is permissible -> halts in non-final state q4."
    )

    doc.add_heading("5. Programming Code in C", level=2)
    p_c4 = doc.add_paragraph()
    r_c4 = p_c4.add_run(
        "/*\n"
        " * Question 4: Turing Machine for L = { 0^n 1^n 0^n | n >= 1 } in C\n"
        " * Simulates exact faculty rules & prints faculty tape trace with ^ and state\n"
        " */\n"
        "#include <stdio.h>\n"
        "#include <string.h>\n"
        "#include <stdbool.h>\n\n"
        "typedef struct { int next_state; char write_sym; char move_dir; bool valid; } Transition;\n"
        "Transition delta_table[6][6]; // States q0..q5, symbols 0, 1, X, Y, Z, B\n\n"
        "void print_tape_trace(int step, int state, const char *tape, int tape_len, int head_pos) {\n"
        "    printf(\"Step %2d | Tape: \", step);\n"
        "    for (int i = 0; i < tape_len; i++) printf(\" %c \", tape[i]);\n"
        "    printf(\"\\n         Head: \");\n"
        "    for (int i = 0; i < head_pos; i++) printf(\"   \");\n"
        "    printf(\" ^ \\n         State:\");\n"
        "    for (int i = 0; i < head_pos; i++) printf(\"   \");\n"
        "    printf(\" q%d\\n\", state);\n"
        "}\n\n"
        "bool simulate_tm(const char *input, const char *desc, bool verbose) {\n"
        "    char tape[128]; int in_len = strlen(input);\n"
        "    for (int i = 0; i < in_len; i++) tape[i] = input[i];\n"
        "    tape[in_len] = 'B'; int tape_len = in_len + 1;\n"
        "    int state = 0, head = 0, steps = 0;\n"
        "    while (steps < 500 && state != 5) {\n"
        "        char cur_sym = (head < tape_len) ? tape[head] : 'B';\n"
        "        int s_idx = sym_to_idx(cur_sym);\n"
        "        if (s_idx < 0 || !delta_table[state][s_idx].valid) break; // Halts\n"
        "        Transition t = delta_table[state][s_idx];\n"
        "        tape[head] = t.write_sym; state = t.next_state;\n"
        "        if (t.move_dir == 'R') { head++; if (head >= tape_len) tape[tape_len++] = 'B'; }\n"
        "        else if (t.move_dir == 'L' && head > 0) head--;\n"
        "        steps++;\n"
        "    }\n"
        "    return (state == 5);\n"
        "}\n"
    )
    r_c4.font.name = "Consolas"
    r_c4.font.size = Pt(8.5)

    doc.add_heading("6. Execution Output & Verification", level=2)
    p_c4_out = doc.add_paragraph()
    r_c4_out = p_c4_out.add_run(
        "=======================================================================\n"
        "Test Case: Test 1: w = 010 (n = 1, Base Valid Case)\n"
        "Input String: w = \"010\"\n"
        "Execution Summary: Total Steps = 8, Final State = q5\n"
        "Result: ACCEPTED (String matches L = { 0^n 1^n 0^n | n >= 1 })\n"
        "-----------------------------------------------------------------------\n"
        "Test Case: Test 2: w = 001100 (n = 2, Core Faculty Sample String)\n"
        "Input String: w = \"001100\"\n"
        "Execution Summary: Total Steps = 23, Final State = q5\n"
        "Result: ACCEPTED (String matches L = { 0^n 1^n 0^n | n >= 1 })\n"
        "-----------------------------------------------------------------------\n"
        "Test Case: Test 4: w = 00110 (Unequal Group Lengths, Rejected)\n"
        "Input String: w = \"00110\"\n"
        "Execution Summary: Total Steps = 13, Final State = q2\n"
        "Result: REJECTED (Machine halted in non-accepting state q2)\n"
        "=======================================================================\n"
        "EXHAUSTIVE VERIFICATION ON ALL BINARY STRINGS UP TO LENGTH 10:\n"
        "Tested 2046 binary strings: 2046 Passed, 0 Mismatches -> 100% VERIFIED!\n"
    )
    r_c4_out.font.name = "Consolas"
    r_c4_out.font.size = Pt(8.5)

    doc.add_heading("7. Implementation in JFLAP (Part d)", level=2)
    doc.add_paragraph(
        "The Turing Machine is implemented in JFLAP (saved as tm_0n1n0n.jff):\n"
        "1. Open JFLAP -> Select 'Turing Machine'.\n"
        "2. Create states q0 (Initial), q1, q2, q3, q4, and q5 (Final).\n"
        "3. Configure transitions in JFLAP format (read ; write , move):\n"
        "   • q0 -> q1:  0 ; X , R\n"
        "   • q0 -> q4:  Y ; Y , R\n"
        "   • q1 -> q1:  0 ; 0 , R   and   Y ; Y , R\n"
        "   • q1 -> q2:  1 ; Y , R\n"
        "   • q2 -> q2:  1 ; 1 , R   and   Z ; Z , R\n"
        "   • q2 -> q3:  0 ; Z , L\n"
        "   • q3 -> q3:  0 ; 0 , L ;  1 ; 1 , L ;  Y ; Y , L ;  Z ; Z , L\n"
        "   • q3 -> q0:  X ; X , R\n"
        "   • q4 -> q4:  Y ; Y , R   and   Z ; Z , R\n"
        "   • q4 -> q5:  □ ; □ , R  (Blank entered as empty field or '_')\n"
        "4. Use 'Step' or 'Fast Run' to inspect tape changes during simulation."
    )

    doc.add_heading("8. Why a Turing Machine is Needed & Computational Capability (Part e)", level=2)
    doc.add_paragraph(
        "1. Proof that L is Not Context-Free (Pumping Lemma for CFLs):\n"
        "   Suppose for contradiction that L = { 0^n 1^n 0^n | n ≥ 1 } is context-free. Let p be the pumping length.\n"
        "   Choose string s = 0^p 1^p 0^p ∈ L, where |s| = 3p ≥ p.\n"
        "   By the Pumping Lemma for CFLs, s can be written as s = uvxyz such that:\n"
        "     (i) |vxy| ≤ p\n"
        "     (ii) |vy| ≥ 1\n"
        "     (iii) For all i ≥ 0, uv^i x y^i z ∈ L.\n"
        "   Because |vxy| ≤ p, the substring vxy can span across at most TWO adjacent groups of symbols (either the first "
        "0s and 1s, or the 1s and second 0s). It cannot contain symbols from all three groups simultaneously.\n"
        "   Therefore, pumping v and y (e.g. for i = 2: uv^2 x y^2 z) increases the count of at most two groups while "
        "the remaining group remains unchanged. Consequently, the three groups no longer have equal length, so uv^2 x y^2 z ∉ L.\n"
        "   This contradiction proves that L is NOT context-free.\n\n"
        "2. Why a Pushdown Automaton Cannot Recognize L:\n"
        "   A PDA has only one stack. While it can match two groups (e.g. 0^n 1^n by pushing 0s and popping on 1s), "
        "emptying the stack destroys the memory of 'n'. When the third group (0^n) arrives, the count information is gone.\n\n"
        "3. Computational Capability of the Turing Machine:\n"
        "   The Turing machine overcomes this fundamental memory limitation through a two-way read/write infinite tape. "
        "It non-destructively marks matching symbols with markers (X, Y, Z) and rewinds across the tape as many times "
        "as necessary. The language L is context-sensitive and decidable; the TM halts in O(n²) steps for all inputs."
    )

    doc.save("ATC_Assignment_BIS503T.docx")
    print("Successfully created ATC_Assignment_BIS503T.docx")

if __name__ == "__main__":
    create_document()

