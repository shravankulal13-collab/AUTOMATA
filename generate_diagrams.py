import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Set font styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'

def draw_circle(ax, x, y, r=0.35, label="", is_final=False, is_start=False, fill_color="#f8f9fa"):
    # Outer circle
    circle = patches.Circle((x, y), r, edgecolor='#1a237e', facecolor=fill_color, linewidth=2, zorder=3)
    ax.add_patch(circle)
    if is_final:
        inner_circle = patches.Circle((x, y), r - 0.07, edgecolor='#1a237e', facecolor='none', linewidth=1.8, zorder=4)
        ax.add_patch(inner_circle)
    # Label
    ax.text(x, y, label, ha='center', va='center', fontsize=13, fontweight='bold', color='#1a237e', zorder=5)
    # Start arrow
    if is_start:
        ax.annotate('Start', xy=(x - r, y), xytext=(x - r - 0.75, y),
                    arrowprops=dict(facecolor='#1a237e', edgecolor='#1a237e', width=1.8, headwidth=7),
                    ha='right', va='center', fontsize=11, fontweight='bold', color='#1a237e', zorder=5)

def draw_q1_dfa():
    fig, ax = plt.subplots(figsize=(10, 4.8), dpi=300)
    ax.set_xlim(-1.5, 8.5)
    ax.set_ylim(-2.2, 2.6)
    ax.axis('off')

    # States positions
    # q0 -> (1, 0), q1 -> (3.5, 0), q2 -> (6, 0)
    # q3 -> (3.5, 1.8), q4 -> (6, -1.5)
    pos = {
        'q0': (1.0, 0.0),
        'q1': (3.5, 0.0),
        'q2': (6.0, 0.0),
        'q3': (3.5, 1.7),
        'q4': (7.5, -0.8)
    }

    # Draw states
    draw_circle(ax, pos['q0'][0], pos['q0'][1], label=r"$q_0$", is_start=True)
    draw_circle(ax, pos['q1'][0], pos['q1'][1], label=r"$q_1$")
    draw_circle(ax, pos['q2'][0], pos['q2'][1], label=r"$q_2$")
    draw_circle(ax, pos['q3'][0], pos['q3'][1], label=r"$q_3$", is_final=True, fill_color="#e8f5e9")
    draw_circle(ax, pos['q4'][0], pos['q4'][1], label=r"$q_4$", fill_color="#ffebee")

    # Annotate labels for states
    ax.text(pos['q3'][0], pos['q3'][1] + 0.5, "ACCESS GRANTED\n(Final State)", ha='center', va='bottom', fontsize=9, color="#2e7d32", fontweight='bold')
    ax.text(pos['q4'][0], pos['q4'][1] - 0.5, "CARD BLOCKED\n(Trap State)", ha='center', va='top', fontsize=9, color="#c62828", fontweight='bold')

    # Transitions
    # q0 -> q1 (W)
    ax.annotate('', xy=(pos['q1'][0]-0.35, pos['q1'][1]), xytext=(pos['q0'][0]+0.35, pos['q0'][1]),
                arrowprops=dict(facecolor='#d32f2f', edgecolor='#d32f2f', width=1.5, headwidth=6), zorder=2)
    ax.text(2.25, 0.15, "W", color="#d32f2f", fontsize=11, fontweight='bold', ha='center')

    # q1 -> q2 (W)
    ax.annotate('', xy=(pos['q2'][0]-0.35, pos['q2'][1]), xytext=(pos['q1'][0]+0.35, pos['q1'][1]),
                arrowprops=dict(facecolor='#d32f2f', edgecolor='#d32f2f', width=1.5, headwidth=6), zorder=2)
    ax.text(4.75, 0.15, "W", color="#d32f2f", fontsize=11, fontweight='bold', ha='center')

    # q2 -> q4 (W)
    ax.annotate('', xy=(pos['q4'][0]-0.25, pos['q4'][1]+0.25), xytext=(pos['q2'][0]+0.25, pos['q2'][1]-0.25),
                arrowprops=dict(facecolor='#d32f2f', edgecolor='#d32f2f', width=1.5, headwidth=6), zorder=2)
    ax.text(6.9, -0.2, "W", color="#d32f2f", fontsize=11, fontweight='bold', ha='center')

    # q0 -> q3 (C)
    ax.annotate('', xy=(pos['q3'][0]-0.3, pos['q3'][1]-0.2), xytext=(pos['q0'][0]+0.2, pos['q0'][1]+0.3),
                arrowprops=dict(arrowstyle="->", color='#2e7d32', lw=1.8, mutation_scale=15), zorder=2)
    ax.text(2.0, 1.1, "C", color="#2e7d32", fontsize=11, fontweight='bold', ha='center')

    # q1 -> q3 (C)
    ax.annotate('', xy=(pos['q3'][0], pos['q3'][1]-0.35), xytext=(pos['q1'][0], pos['q1'][1]+0.35),
                arrowprops=dict(arrowstyle="->", color='#2e7d32', lw=1.8, mutation_scale=15), zorder=2)
    ax.text(3.7, 0.85, "C", color="#2e7d32", fontsize=11, fontweight='bold', ha='left')

    # q2 -> q3 (C)
    ax.annotate('', xy=(pos['q3'][0]+0.3, pos['q3'][1]-0.2), xytext=(pos['q2'][0]-0.2, pos['q2'][1]+0.3),
                arrowprops=dict(arrowstyle="->", color='#2e7d32', lw=1.8, mutation_scale=15), zorder=2)
    ax.text(5.0, 1.1, "C", color="#2e7d32", fontsize=11, fontweight='bold', ha='center')

    # q3 self loop (C, W)
    arc_q3 = patches.Arc((pos['q3'][0], pos['q3'][1]+0.35), 0.7, 0.7, angle=0, theta1=20, theta2=160, color='#1a237e', lw=1.8)
    ax.add_patch(arc_q3)
    ax.annotate('', xy=(pos['q3'][0]+0.25, pos['q3'][1]+0.35), xytext=(pos['q3'][0]+0.24, pos['q3'][1]+0.4),
                arrowprops=dict(arrowstyle="->", color='#1a237e', lw=1.8, mutation_scale=15))
    ax.text(pos['q3'][0], pos['q3'][1]+0.85, "C, W", color="#1a237e", fontsize=10, fontweight='bold', ha='center')

    # q4 self loop (C, W)
    arc_q4 = patches.Arc((pos['q4'][0], pos['q4'][1]-0.35), 0.7, 0.7, angle=0, theta1=200, theta2=340, color='#1a237e', lw=1.8)
    ax.add_patch(arc_q4)
    ax.annotate('', xy=(pos['q4'][0]+0.25, pos['q4'][1]-0.35), xytext=(pos['q4'][0]+0.24, pos['q4'][1]-0.4),
                arrowprops=dict(arrowstyle="->", color='#1a237e', lw=1.8, mutation_scale=15))
    ax.text(pos['q4'][0], pos['q4'][1]-0.95, "C, W", color="#1a237e", fontsize=10, fontweight='bold', ha='center')

    plt.title(r"State Transition Diagram: ATM PIN Verification DFA  $A = (\{q_0, q_1, q_2, q_3, q_4\}, \{C, W\}, \delta, q_0, \{q_3\})$",
              fontsize=12, fontweight='bold', pad=15, color='#0d47a1')
    plt.tight_layout()
    plt.savefig("q1_atm_dfa.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved q1_atm_dfa.png")

def draw_q3_pda():
    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=300)
    ax.set_xlim(-1.5, 9.0)
    ax.set_ylim(-2.0, 2.5)
    ax.axis('off')

    pos = {
        'q0': (1.5, 0.0),
        'q1': (5.5, 0.0)
    }

    draw_circle(ax, pos['q0'][0], pos['q0'][1], label=r"$q_0$", is_start=True)
    draw_circle(ax, pos['q1'][0], pos['q1'][1], label=r"$q_1$", is_final=True, fill_color="#e8f5e9")

    # Loops on q0:
    # o, Z0 / OZ0
    # o, O / OO
    # p, O / epsilon
    arc_q0 = patches.Arc((pos['q0'][0], pos['q0'][1]+0.35), 1.0, 1.0, angle=0, theta1=20, theta2=160, color='#1a237e', lw=2)
    ax.add_patch(arc_q0)
    ax.annotate('', xy=(pos['q0'][0]+0.35, pos['q0'][1]+0.35), xytext=(pos['q0'][0]+0.34, pos['q0'][1]+0.42),
                arrowprops=dict(arrowstyle="->", color='#1a237e', lw=2, mutation_scale=15))

    ax.text(pos['q0'][0], pos['q0'][1]+1.0, "o , Z0 / OZ0\no , O / OO\np , O / \u03b5",
            color="#0d47a1", fontsize=10.5, fontweight='bold', ha='center', va='bottom', linespacing=1.3)

    # Arrow q0 -> q1 labelled epsilon, Z0 / Z0
    ax.annotate('', xy=(pos['q1'][0]-0.35, pos['q1'][1]), xytext=(pos['q0'][0]+0.35, pos['q0'][1]),
                arrowprops=dict(facecolor='#1a237e', edgecolor='#1a237e', width=1.8, headwidth=7), zorder=2)
    ax.text(3.5, 0.25, "\u03b5 , Z0 / Z0", color="#1a237e", fontsize=11, fontweight='bold', ha='center')

    # Draw Stack Box Representation beside diagram
    stack_x = 7.5
    stack_y = -0.8
    stack_w = 1.0
    stack_h = 1.8

    # Stack open at top (draw 3 walls)
    ax.plot([stack_x, stack_x, stack_x + stack_w, stack_x + stack_w],
            [stack_y + stack_h, stack_y, stack_y, stack_y + stack_h],
            color='#37474f', lw=2.5)

    # Stack cells
    ax.plot([stack_x, stack_x + stack_w], [stack_y + 0.6, stack_y + 0.6], color='#90a4ae', lw=1.5, ls='--')
    ax.plot([stack_x, stack_x + stack_w], [stack_y + 1.2, stack_y + 1.2], color='#90a4ae', lw=1.5, ls='--')

    ax.text(stack_x + stack_w/2, stack_y + 0.3, "Z0", ha='center', va='center', fontsize=11, fontweight='bold', color='#b71c1c')
    ax.text(stack_x + stack_w/2, stack_y + 0.9, "O", ha='center', va='center', fontsize=11, fontweight='bold', color='#1565c0')
    ax.text(stack_x + stack_w/2, stack_y + 1.5, "O", ha='center', va='center', fontsize=11, fontweight='bold', color='#1565c0')

    ax.text(stack_x + stack_w/2, stack_y - 0.35, "Stack Memory\n(Bottom = Z0)", ha='center', va='top', fontsize=9.5, fontweight='bold', color='#37474f')
    ax.annotate('Top of Stack\n(Pushed/Popped)', xy=(stack_x + stack_w, stack_y + 1.5), xytext=(stack_x + stack_w + 0.4, stack_y + 1.7),
                arrowprops=dict(arrowstyle="->", color='#37474f', lw=1.2), fontsize=8.5, color='#37474f')

    plt.title(r"Pushdown Automaton (PDA) Transition Diagram: $P = (\{q_0, q_1\}, \{o, p\}, \{O, Z_0\}, \delta, q_0, Z_0, \{q_1\})$",
              fontsize=11.5, fontweight='bold', pad=15, color='#0d47a1')
    plt.tight_layout()
    plt.savefig("q3_order_pda.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved q3_order_pda.png")

def draw_q4_tm():
    fig, ax = plt.subplots(figsize=(11, 5.2), dpi=300)
    ax.set_xlim(-1.5, 10.5)
    ax.set_ylim(-3.0, 3.0)
    ax.axis('off')

    # q0 at (1, 0), q1 at (3.5, 1.5), q2 at (6.5, 1.5), q3 at (5.0, -1.8), q4 at (7.5, 0.0), q5 at (9.8, 0.0)
    pos = {
        'q0': (1.0, 0.0),
        'q1': (3.5, 1.5),
        'q2': (6.5, 1.5),
        'q3': (5.0, -1.7),
        'q4': (7.5, 0.0),
        'q5': (9.8, 0.0)
    }

    draw_circle(ax, pos['q0'][0], pos['q0'][1], label=r"$q_0$", is_start=True)
    draw_circle(ax, pos['q1'][0], pos['q1'][1], label=r"$q_1$")
    draw_circle(ax, pos['q2'][0], pos['q2'][1], label=r"$q_2$")
    draw_circle(ax, pos['q3'][0], pos['q3'][1], label=r"$q_3$")
    draw_circle(ax, pos['q4'][0], pos['q4'][1], label=r"$q_4$")
    draw_circle(ax, pos['q5'][0], pos['q5'][1], label=r"$q_5$", is_final=True, fill_color="#e8f5e9")

    # q0 -> q1: 0 / X, R
    ax.annotate('', xy=(pos['q1'][0]-0.25, pos['q1'][1]-0.25), xytext=(pos['q0'][0]+0.25, pos['q0'][1]+0.25),
                arrowprops=dict(facecolor='#1a237e', edgecolor='#1a237e', width=1.5, headwidth=6))
    ax.text(2.0, 0.95, "0 / X , R", color="#1a237e", fontsize=10.5, fontweight='bold', ha='center', rotation=30)

    # q0 -> q4: Y / Y, R
    ax.annotate('', xy=(pos['q4'][0]-0.35, pos['q4'][1]), xytext=(pos['q0'][0]+0.35, pos['q0'][1]),
                arrowprops=dict(facecolor='#1a237e', edgecolor='#1a237e', width=1.5, headwidth=6))
    ax.text(4.25, 0.15, "Y / Y , R", color="#1a237e", fontsize=10.5, fontweight='bold', ha='center')

    # q1 loop: 0 / 0, R ; Y / Y, R
    arc_q1 = patches.Arc((pos['q1'][0], pos['q1'][1]+0.35), 0.8, 0.8, angle=0, theta1=20, theta2=160, color='#1a237e', lw=1.8)
    ax.add_patch(arc_q1)
    ax.annotate('', xy=(pos['q1'][0]+0.28, pos['q1'][1]+0.35), xytext=(pos['q1'][0]+0.27, pos['q1'][1]+0.42),
                arrowprops=dict(arrowstyle="->", color='#1a237e', lw=1.8, mutation_scale=15))
    ax.text(pos['q1'][0], pos['q1'][1]+0.9, "0 / 0 , R\nY / Y , R", color="#1a237e", fontsize=9.5, fontweight='bold', ha='center')

    # q1 -> q2: 1 / Y, R
    ax.annotate('', xy=(pos['q2'][0]-0.35, pos['q2'][1]), xytext=(pos['q1'][0]+0.35, pos['q1'][1]),
                arrowprops=dict(facecolor='#1a237e', edgecolor='#1a237e', width=1.5, headwidth=6))
    ax.text(5.0, 1.65, "1 / Y , R", color="#1a237e", fontsize=10.5, fontweight='bold', ha='center')

    # q2 loop: 1 / 1, R ; Z / Z, R
    arc_q2 = patches.Arc((pos['q2'][0], pos['q2'][1]+0.35), 0.8, 0.8, angle=0, theta1=20, theta2=160, color='#1a237e', lw=1.8)
    ax.add_patch(arc_q2)
    ax.annotate('', xy=(pos['q2'][0]+0.28, pos['q2'][1]+0.35), xytext=(pos['q2'][0]+0.27, pos['q2'][1]+0.42),
                arrowprops=dict(arrowstyle="->", color='#1a237e', lw=1.8, mutation_scale=15))
    ax.text(pos['q2'][0], pos['q2'][1]+0.9, "1 / 1 , R\nZ / Z , R", color="#1a237e", fontsize=9.5, fontweight='bold', ha='center')

    # q2 -> q3: 0 / Z, L
    ax.annotate('', xy=(pos['q3'][0]+0.25, pos['q3'][1]+0.25), xytext=(pos['q2'][0]-0.25, pos['q2'][1]-0.25),
                arrowprops=dict(facecolor='#1a237e', edgecolor='#1a237e', width=1.5, headwidth=6))
    ax.text(6.0, -0.2, "0 / Z , L", color="#1a237e", fontsize=10.5, fontweight='bold', ha='center', rotation=60)

    # q3 loop: 0/0,L; 1/1,L; Y/Y,L; Z/Z,L (underneath)
    arc_q3 = patches.Arc((pos['q3'][0], pos['q3'][1]-0.35), 1.0, 1.0, angle=0, theta1=200, theta2=340, color='#1a237e', lw=1.8)
    ax.add_patch(arc_q3)
    ax.annotate('', xy=(pos['q3'][0]+0.35, pos['q3'][1]-0.35), xytext=(pos['q3'][0]+0.34, pos['q3'][1]-0.42),
                arrowprops=dict(arrowstyle="->", color='#1a237e', lw=1.8, mutation_scale=15))
    ax.text(pos['q3'][0], pos['q3'][1]-1.1, "0 / 0 , L ; 1 / 1 , L\nY / Y , L ; Z / Z , L", color="#1a237e", fontsize=9, fontweight='bold', ha='center')

    # q3 -> q0: X / X, R
    ax.annotate('', xy=(pos['q0'][0]+0.2, pos['q0'][1]-0.25), xytext=(pos['q3'][0]-0.25, pos['q3'][1]+0.2),
                arrowprops=dict(facecolor='#1a237e', edgecolor='#1a237e', width=1.5, headwidth=6))
    ax.text(2.6, -1.0, "X / X , R", color="#1a237e", fontsize=10.5, fontweight='bold', ha='center', rotation=-25)

    # q4 loop: Y / Y, R ; Z / Z, R
    arc_q4 = patches.Arc((pos['q4'][0], pos['q4'][1]+0.35), 0.8, 0.8, angle=0, theta1=20, theta2=160, color='#1a237e', lw=1.8)
    ax.add_patch(arc_q4)
    ax.annotate('', xy=(pos['q4'][0]+0.28, pos['q4'][1]+0.35), xytext=(pos['q4'][0]+0.27, pos['q4'][1]+0.42),
                arrowprops=dict(arrowstyle="->", color='#1a237e', lw=1.8, mutation_scale=15))
    ax.text(pos['q4'][0], pos['q4'][1]+0.9, "Y / Y , R\nZ / Z , R", color="#1a237e", fontsize=9.5, fontweight='bold', ha='center')

    # q4 -> q5: B / B, R
    ax.annotate('', xy=(pos['q5'][0]-0.35, pos['q5'][1]), xytext=(pos['q4'][0]+0.35, pos['q4'][1]),
                arrowprops=dict(facecolor='#1a237e', edgecolor='#1a237e', width=1.5, headwidth=6))
    ax.text(8.65, 0.15, "B / B , R", color="#1a237e", fontsize=10.5, fontweight='bold', ha='center')

    plt.title(r"Turing Machine Transition Diagram: $M = (\{q_0, q_1, q_2, q_3, q_4, q_5\}, \{0, 1\}, \{0, 1, X, Y, Z, B\}, \delta, q_0, B, \{q_5\})$",
              fontsize=11.5, fontweight='bold', pad=15, color='#0d47a1')
    plt.tight_layout()
    plt.savefig("q4_tm_0n1n0n.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved q4_tm_0n1n0n.png")

if __name__ == "__main__":
    draw_q1_dfa()
    draw_q3_pda()
    draw_q4_tm()

