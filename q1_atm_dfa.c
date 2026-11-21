/*
 * Course: Automata Theory and Computability (BIS503T)
 * Question 1: Automated ATM PIN Verification System using DFA
 * Faculty Notation: States q0, q1, q2, q3, q4
 * Alphabet: Sigma = { C, W } (C = Correct PIN attempt, W = Wrong PIN attempt)
 * Start State: -> q0
 * Final State: * q3 (ACCESS GRANTED)
 * Trap State:  q4 (CARD BLOCKED)
 */

#include <stdio.h>
#include <string.h>

#define NUM_STATES 5
#define NUM_SYMBOLS 2

// State indices: q0=0, q1=1, q2=2, q3=3, q4=4
const char *state_names[NUM_STATES] = {"q0", "q1", "q2", "q3", "q4"};

// Transition table: delta[state][symbol]
// Symbol 0 = 'C' (Correct), Symbol 1 = 'W' (Wrong)
int delta[NUM_STATES][NUM_SYMBOLS] = {
    {3, 1}, // -> q0: on C -> q3, on W -> q1
    {3, 2}, //    q1: on C -> q3, on W -> q2
    {3, 4}, //    q2: on C -> q3, on W -> q4
    {3, 3}, //  * q3: on C -> q3, on W -> q3 (absorbing / granted)
    {4, 4}  //    q4: on C -> q4, on W -> q4 (trap / blocked)
};

void print_transition_table() {
    printf("====================================================\n");
    printf("         ATM PIN VERIFICATION DFA TABLE             \n");
    printf("====================================================\n");
    printf("   delta  |   C (Correct)   |   W (Wrong)          \n");
    printf("----------------------------------------------------\n");
    printf(" -> q0    |      q3         |      q1              \n");
    printf("    q1    |      q3         |      q2              \n");
    printf("    q2    |      q3         |      q4              \n");
    printf("  * q3    |      q3         |      q3  (ACCESS GRANTED)\n");
    printf("    q4    |      q4         |      q4  (CARD BLOCKED)  \n");
    printf("====================================================\n\n");
}

int map_symbol(char ch) {
    if (ch == 'C' || ch == 'c') return 0;
    if (ch == 'W' || ch == 'w') return 1;
    return -1;
}

// Simulates the DFA on an input string of C's and W's
int simulate_dfa(const char *input, const char *scenario_name) {
    int current_state = 0; // start at q0
    printf("----------------------------------------------------\n");
    printf("Test Case: %s\n", scenario_name);
    printf("Input Sequence: %s\n", input);
    printf("State Transition Path:\n  %s", state_names[current_state]);

    int len = strlen(input);
    for (int i = 0; i < len; i++) {
        int sym = map_symbol(input[i]);
        if (sym == -1) {
            printf("\n[ERROR] Invalid input symbol '%c'. Expected 'C' or 'W'.\n", input[i]);
            return -1;
        }
        current_state = delta[current_state][sym];
        printf(" --(%c)--> %s", input[i], state_names[current_state]);
    }
    printf("\n");

    printf("Final State: %s\n", state_names[current_state]);
    if (current_state == 3) {
        printf("Result: ACCEPTED => ACCESS GRANTED (Authentication Successful)\n");
        return 1;
    } else if (current_state == 4) {
        printf("Result: REJECTED => CARD BLOCKED (3 Failed Attempts Reached)\n");
        return 0;
    } else {
        printf("Result: INCOMPLETE => Waiting for further attempts (Remaining: %d)\n", 3 - current_state);
        return 0;
    }
}

// Helper to simulate interactive 4-digit PIN entries
void simulate_pin_entry() {
    const char correct_pin[] = "1234";
    char entered_pin[10];
    char symbol_stream[10] = "";
    int stream_idx = 0;

    printf("\n====================================================\n");
    printf("      INTERACTIVE 4-DIGIT PIN VERIFICATION DEMO     \n");
    printf("      Predefined PIN in ATM: %s                     \n", correct_pin);
    printf("====================================================\n");

    const char *test_pins[4] = {"1111", "2222", "1234", "9999"};
    printf("Simulating user entering attempts: 1111, then 2222, then 1234...\n\n");

    for (int attempt = 1; attempt <= 3; attempt++) {
        const char *pin = test_pins[attempt - 1];
        printf("[Attempt %d] User types: %s", attempt, pin);
        if (strcmp(pin, correct_pin) == 0) {
            printf(" -> CORRECT PIN entered! Generated symbol: 'C'\n");
            symbol_stream[stream_idx++] = 'C';
            symbol_stream[stream_idx] = '\0';
            break;
        } else {
            printf(" -> WRONG PIN entered! Generated symbol: 'W'\n");
            symbol_stream[stream_idx++] = 'W';
            symbol_stream[stream_idx] = '\0';
        }
    }
    simulate_dfa(symbol_stream, "Interactive ATM Run (Mapped to DFA symbols)");
}

int main() {
    print_transition_table();

    // 5 Required / Standard Test Cases
    simulate_dfa("C", "Scenario 1: Correct PIN on First Attempt");
    simulate_dfa("WC", "Scenario 2: One Wrong Attempt, then Correct PIN");
    simulate_dfa("WWW", "Scenario 3: Three Consecutive Wrong Attempts (Card Blocked)");
    simulate_dfa("WWC", "Scenario 4: Two Wrong Attempts, Correct on Third Attempt");
    simulate_dfa("WWWC", "Scenario 5: Fourth Attempt Entered After Card is Blocked");
    simulate_dfa("CW", "Scenario 6: Access Granted, Subsequent Activity Absorbed");

    simulate_pin_entry();

    printf("\n====================================================\n");
    printf("DFA Simulation Completed Successfully.\n");
    printf("====================================================\n");
    return 0;
}

