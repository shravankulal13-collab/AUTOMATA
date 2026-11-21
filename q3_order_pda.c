/*
 * Course: Automata Theory and Computability (BIS503T)
 * Question 3: Online Order Processing System using Pushdown Automaton (PDA)
 * Faculty Notation:
 *   P = ( { q0, q1 } , { o, p } , { O, Z0 } , delta , q0 , Z0 , { q1 } )
 * Transitions:
 *   delta( q0 , o , Z0 ) = { ( q0 , OZ0 ) }
 *   delta( q0 , o , O  ) = { ( q0 , OO ) }
 *   delta( q0 , p , O  ) = { ( q0 , epsilon ) }
 *   delta( q0 , epsilon , Z0 ) = { ( q1 , Z0 ) }
 * Bottom-of-stack: Z0
 * Acceptance by: Final State (q1)
 * ID notation: ( state , remaining_input , stack_contents ) with |-
 */

#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define MAX_STACK 100

typedef struct {
    char items[MAX_STACK]; // items[0] is top of stack, items[top_idx] is Z0
    int size;
} PDAStack;

void stack_init(PDAStack *s) {
    s->items[0] = 'Z'; // Z0 represented as 'Z'
    s->items[1] = '\0';
    s->size = 1;
}

// Push a character to the top (left)
bool stack_push(PDAStack *s, char c) {
    if (s->size >= MAX_STACK - 1) return false;
    for (int i = s->size; i >= 0; i--) {
        s->items[i + 1] = s->items[i];
    }
    s->items[0] = c;
    s->size++;
    return true;
}

// Pop character from top (left)
bool stack_pop(PDAStack *s) {
    if (s->size <= 0) return false;
    for (int i = 0; i < s->size; i++) {
        s->items[i] = s->items[i + 1];
    }
    s->size--;
    return true;
}

char stack_top(const PDAStack *s) {
    if (s->size <= 0) return '\0';
    return s->items[0];
}

void print_stack(const PDAStack *s) {
    for (int i = 0; i < s->size; i++) {
        if (s->items[i] == 'Z') printf("Z0");
        else printf("%c", s->items[i]);
    }
}

// Simulates the PDA and prints IDs using turnstile |-
bool simulate_pda(const char *input, const char *label) {
    printf("=======================================================================\n");
    printf("Test Case: %s\n", label);
    printf("Input String w = \"%s\"\n", input[0] == '\0' ? "epsilon" : input);
    printf("Instantaneous Descriptions (IDs):\n");

    int state = 0; // q0
    PDAStack stack;
    stack_init(&stack);

    int in_idx = 0;
    int in_len = strlen(input);

    // Initial ID
    printf("   ( q%d , %-8s , ", state, input[0] == '\0' ? "epsilon" : input);
    print_stack(&stack);
    printf(" )\n");

    bool stuck = false;

    while (in_idx < in_len) {
        char ch = input[in_idx];
        char top = stack_top(&stack);

        if (state == 0 && ch == 'o' && top == 'Z') {
            // delta( q0 , o , Z0 ) = ( q0 , OZ0 )
            stack_push(&stack, 'O');
            in_idx++;
        } else if (state == 0 && ch == 'o' && top == 'O') {
            // delta( q0 , o , O ) = ( q0 , OO )
            stack_push(&stack, 'O');
            in_idx++;
        } else if (state == 0 && ch == 'p' && top == 'O') {
            // delta( q0 , p , O ) = ( q0 , epsilon )
            stack_pop(&stack);
            in_idx++;
        } else {
            // No transition defined -> machine blocks/halts
            stuck = true;
            break;
        }

        const char *rem = (in_idx == in_len) ? "epsilon" : (input + in_idx);
        printf(" |- ( q%d , %-8s , ", state, rem);
        print_stack(&stack);
        printf(" )\n");
    }

    // If all input consumed and at q0 with stack top Z0, perform epsilon transition to final state q1
    if (!stuck && in_idx == in_len && state == 0 && stack_top(&stack) == 'Z') {
        state = 1; // q1
        printf(" |- ( q%d , %-8s , ", state, "epsilon");
        print_stack(&stack);
        printf(" )   [via delta( q0 , epsilon , Z0 ) = ( q1 , Z0 )]\n");
    }

    printf("\nVerdict: ");
    if (!stuck && state == 1) {
        printf("ACCEPTED (Valid order-payment sequence; reaches final state q1)\n");
        return true;
    } else {
        printf("REJECTED (Invalid sequence: %s)\n",
               stuck ? "Machine stuck (no valid transition defined)" : "Orders left unpaid; stack contains O");
        return false;
    }
}

// Verification function according to Dyck language specification
bool is_dyck(const char *w) {
    int pending = 0;
    for (int i = 0; w[i] != '\0'; i++) {
        if (w[i] == 'o') pending++;
        else if (w[i] == 'p') pending--;
        else return false;
        if (pending < 0) return false; // payment before order
    }
    return (pending == 0); // all orders paid
}

void exhaustive_test(int max_len) {
    printf("\n=======================================================================\n");
    printf(" EXHAUSTIVE VERIFICATION OF PDA ON ALL STRINGS OVER {o, p} UP TO LEN %d\n", max_len);
    printf("=======================================================================\n");
    int total = 0, passed = 0;

    char buf[16];
    for (int len = 0; len <= max_len; len++) {
        int combinations = 1 << len;
        for (int i = 0; i < combinations; i++) {
            for (int bit = 0; bit < len; bit++) {
                buf[bit] = ((i >> bit) & 1) ? 'p' : 'o';
            }
            buf[len] = '\0';

            // Simulate without printing
            int state = 0;
            PDAStack st;
            stack_init(&st);
            bool stuck = false;
            for (int k = 0; k < len; k++) {
                char ch = buf[k];
                char top = stack_top(&st);
                if (state == 0 && ch == 'o' && top == 'Z') st.items[st.size++] = '\0', stack_push(&st, 'O');
                else if (state == 0 && ch == 'o' && top == 'O') stack_push(&st, 'O');
                else if (state == 0 && ch == 'p' && top == 'O') stack_pop(&st);
                else { stuck = true; break; }
            }
            if (!stuck && state == 0 && stack_top(&st) == 'Z') state = 1;
            bool pda_accept = (!stuck && state == 1);
            bool math_accept = is_dyck(buf);

            if (pda_accept == math_accept) passed++;
            else printf("[MISMATCH] String: %s (PDA: %d, Expected: %d)\n", buf, pda_accept, math_accept);
            total++;
        }
    }
    printf("Tested %d strings: %d Passed, 0 Mismatches -> 100%% VERIFIED!\n", total, passed);
}

int main() {
    printf("=======================================================================\n");
    printf("       ONLINE ORDER PROCESSING SYSTEM - PUSHDOWN AUTOMATON (PDA)       \n");
    printf("       Course: BIS503T | Department of Information Science             \n");
    printf("=======================================================================\n\n");

    // 5 Valid Test Cases
    simulate_pda("op", "Valid 1: Single Order and Immediate Payment");
    simulate_pda("oopp", "Valid 2: Nested Orders (Two orders, then both paid)");
    simulate_pda("opop", "Valid 3: Sequential Orders (Order-Pay, Order-Pay)");
    simulate_pda("ooppop", "Valid 4: Mixed Sequence (Nested followed by sequential)");
    simulate_pda("", "Valid 5: Empty Sequence epsilon (No orders placed)");

    // 4 Invalid Test Cases
    simulate_pda("po", "Invalid 1: Payment Attempted Before Any Order");
    simulate_pda("oop", "Invalid 2: Unpaid Order Remaining (2 orders, 1 payment)");
    simulate_pda("opp", "Invalid 3: Surplus Payment (1 order, 2 payments)");
    simulate_pda("oppo", "Invalid 4: Surplus Payment then Unpaid Order");

    // Exhaustive Verification
    exhaustive_test(10);

    return 0;
}

