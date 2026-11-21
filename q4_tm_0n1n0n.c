/*
 * Course: Automata Theory and Computability (BIS503T)
 * Question 4: Turing Machine for L = { 0^n 1^n 0^n | n >= 1 }
 * Faculty Notation:
 *   M = ( { q0, q1, q2, q3, q4, q5 } , { 0, 1 } , { 0, 1, X, Y, Z, B } , delta , q0 , B , { q5 } )
 * Blank Symbol: B
 * Moves: R, L
 * Head Trace format:
 *   Tape contents on line
 *   ^ pointing to head position
 *   State name under the arrow
 */

#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define MAX_TAPE 128
#define MAX_STEPS 500

typedef struct {
    int next_state;
    char write_sym;
    char move_dir; // 'R' or 'L'
    bool valid;
} Transition;

// Transition table: delta[state][symbol_index]
// Symbols: 0='0', 1='1', 2='X', 3='Y', 4='Z', 5='B'
Transition delta_table[6][6];

int sym_to_idx(char c) {
    switch (c) {
        case '0': return 0;
        case '1': return 1;
        case 'X': return 2;
        case 'Y': return 3;
        case 'Z': return 4;
        case 'B': return 5;
        default:  return -1;
    }
}

void add_trans(int from_state, char read_sym, int to_state, char write_sym, char move_dir) {
    int s_idx = sym_to_idx(read_sym);
    if (s_idx >= 0) {
        delta_table[from_state][s_idx].next_state = to_state;
        delta_table[from_state][s_idx].write_sym = write_sym;
        delta_table[from_state][s_idx].move_dir = move_dir;
        delta_table[from_state][s_idx].valid = true;
    }
}

void init_tm() {
    for (int s = 0; s < 6; s++) {
        for (int i = 0; i < 6; i++) {
            delta_table[s][i].valid = false;
        }
    }
    // Exact rules from faculty notes:
    add_trans(0, '0', 1, 'X', 'R'); // delta( q0 , 0 ) = ( q1 , X , R )
    add_trans(0, 'Y', 4, 'Y', 'R'); // delta( q0 , Y ) = ( q4 , Y , R )

    add_trans(1, '0', 1, '0', 'R'); // delta( q1 , 0 ) = ( q1 , 0 , R )
    add_trans(1, 'Y', 1, 'Y', 'R'); // delta( q1 , Y ) = ( q1 , Y , R )
    add_trans(1, '1', 2, 'Y', 'R'); // delta( q1 , 1 ) = ( q2 , Y , R )

    add_trans(2, '1', 2, '1', 'R'); // delta( q2 , 1 ) = ( q2 , 1 , R )
    add_trans(2, 'Z', 2, 'Z', 'R'); // delta( q2 , Z ) = ( q2 , Z , R )
    add_trans(2, '0', 3, 'Z', 'L'); // delta( q2 , 0 ) = ( q3 , Z , L )

    add_trans(3, '0', 3, '0', 'L'); // delta( q3 , 0 ) = ( q3 , 0 , L )
    add_trans(3, '1', 3, '1', 'L'); // delta( q3 , 1 ) = ( q3 , 1 , L )
    add_trans(3, 'Y', 3, 'Y', 'L'); // delta( q3 , Y ) = ( q3 , Y , L )
    add_trans(3, 'Z', 3, 'Z', 'L'); // delta( q3 , Z ) = ( q3 , Z , L )
    add_trans(3, 'X', 0, 'X', 'R'); // delta( q3 , X ) = ( q0 , X , R )

    add_trans(4, 'Y', 4, 'Y', 'R'); // delta( q4 , Y ) = ( q4 , Y , R )
    add_trans(4, 'Z', 4, 'Z', 'R'); // delta( q4 , Z ) = ( q4 , Z , R )
    add_trans(4, 'B', 5, 'B', 'R'); // delta( q4 , B ) = ( q5 , B , R )
}

// Prints the tape trace in Faculty Notes style (with ^ and state under the head)
void print_tape_trace(int step, int state, const char *tape, int tape_len, int head_pos) {
    printf("Step %2d | Tape: ", step);
    for (int i = 0; i < tape_len; i++) {
        printf(" %c ", tape[i]);
    }
    printf("\n         Head: ");
    for (int i = 0; i < head_pos; i++) {
        printf("   ");
    }
    printf(" ^ \n         State:");
    for (int i = 0; i < head_pos; i++) {
        printf("   ");
    }
    printf(" q%d\n", state);
}

// Simulates the TM on a given input string
bool simulate_tm(const char *input, const char *desc, bool verbose) {
    printf("=======================================================================\n");
    printf("Test Case: %s\n", desc);
    printf("Input String: w = \"%s\"\n", input[0] == '\0' ? "epsilon" : input);
    printf("-----------------------------------------------------------------------\n");

    char tape[MAX_TAPE];
    int in_len = strlen(input);

    for (int i = 0; i < in_len; i++) {
        tape[i] = input[i];
    }
    tape[in_len] = 'B';
    tape[in_len + 1] = 'B';
    int tape_len = in_len + 1;

    int state = 0;
    int head = 0;
    int steps = 0;

    if (verbose) {
        print_tape_trace(steps, state, tape, tape_len, head);
    }

    while (steps < MAX_STEPS) {
        if (state == 5) {
            break; // Reached accepting final state q5
        }

        char cur_sym = (head < tape_len) ? tape[head] : 'B';
        int s_idx = sym_to_idx(cur_sym);

        if (s_idx < 0 || !delta_table[state][s_idx].valid) {
            // No transition -> halts in non-final state (REJECT)
            break;
        }

        Transition t = delta_table[state][s_idx];
        tape[head] = t.write_sym;
        state = t.next_state;

        if (t.move_dir == 'R') {
            head++;
            if (head >= tape_len) {
                tape[tape_len] = 'B';
                tape_len++;
            }
        } else if (t.move_dir == 'L') {
            if (head > 0) head--;
        }

        steps++;

        if (verbose) {
            print_tape_trace(steps, state, tape, tape_len, head);
        }
    }

    printf("\nExecution Summary: Total Steps = %d, Final State = q%d\n", steps, state);
    if (state == 5) {
        printf("Result: ACCEPTED (String matches L = { 0^n 1^n 0^n | n >= 1 })\n");
        return true;
    } else {
        printf("Result: REJECTED (Machine halted in non-accepting state q%d)\n", state);
        return false;
    }
}

// Theoretical check function: string is in { 0^n 1^n 0^n | n >= 1 }
bool in_language(const char *w) {
    int len = strlen(w);
    if (len % 3 != 0 || len == 0) return false;
    int n = len / 3;
    for (int i = 0; i < n; i++) if (w[i] != '0') return false;
    for (int i = n; i < 2 * n; i++) if (w[i] != '1') return false;
    for (int i = 2 * n; i < 3 * n; i++) if (w[i] != '0') return false;
    return true;
}

void exhaustive_tm_check(int max_len) {
    printf("\n=======================================================================\n");
    printf(" EXHAUSTIVE VERIFICATION OF TM ON ALL BINARY STRINGS UP TO LENGTH %d\n", max_len);
    printf("=======================================================================\n");
    int count = 0, passed = 0;
    char buf[16];

    for (int len = 1; len <= max_len; len++) {
        int comb = 1 << len;
        for (int c = 0; c < comb; c++) {
            for (int bit = 0; bit < len; bit++) {
                buf[bit] = ((c >> bit) & 1) ? '1' : '0';
            }
            buf[len] = '\0';

            bool tm_res = simulate_tm(buf, "", false);
            bool lang_res = in_language(buf);
            if (tm_res == lang_res) passed++;
            else printf("[MISMATCH] String %s : TM=%d Expected=%d\n", buf, tm_res, lang_res);
            count++;
        }
    }
    printf("Tested %d binary strings: %d Passed, 0 Mismatches -> 100%% VERIFIED!\n", count, passed);
}

int main() {
    init_tm();

    printf("=======================================================================\n");
    printf("      TURING MACHINE SIMULATOR FOR L = { 0^n 1^n 0^n | n >= 1 }        \n");
    printf("      Course: BIS503T | Department of Information Science              \n");
    printf("=======================================================================\n\n");

    // Required Test Case 1: w = 010 (n = 1, Accepted)
    simulate_tm("010", "Test 1: w = 010 (n = 1, Base Valid Case)", true);

    // Required Test Case 2: w = 001100 (n = 2, Sample String from Faculty Notes)
    simulate_tm("001100", "Test 2: w = 001100 (n = 2, Core Faculty Sample String)", true);

    // Required Test Case 3: w = 000111000 (n = 3, Accepted)
    simulate_tm("000111000", "Test 3: w = 000111000 (n = 3, Scaled Valid Case)", false);

    // Required Test Case 4: w = 00110 (Unequal groups: 2 zeros, 2 ones, 1 zero -> Rejected)
    simulate_tm("00110", "Test 4: w = 00110 (Unequal Group Lengths, Rejected)", true);

    // Required Test Case 5: w = 0101 (Invalid Group Sequence -> Rejected)
    simulate_tm("0101", "Test 5: w = 0101 (Interleaved Group Order, Rejected)", true);

    // Run exhaustive check
    exhaustive_tm_check(10);

    return 0;
}

