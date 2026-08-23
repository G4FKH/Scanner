#---------------------------------------------------------------------------------------
# Name:        Bloc Diagram of Scanner workings
# Purpose:
#
# Author:      g4fkh
#
# Created:     12/07/2026
# Copyright:   (c) g4fkh 2026
# Licence:     <your licence>
#---------------------------------------------------------------------------------------

# Save diagram to: C:\Radio\Python_Scripts\Scanner_block_diagram.png

import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig = plt.figure(figsize=(9, 6))   # Balanced height and width
ax = fig.add_subplot(111)
ax.axis('off')

# Fixed coordinate system
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)

def add_box(x, y, w, h, label):
    rect = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.25",
        linewidth=1.2,
        edgecolor="black",
        facecolor="#e8e8e8"
    )
    ax.add_patch(rect)
    ax.text(
        x + w/2, y + h/2, label,
        ha='center', va='center',
        fontsize=10,
        wrap=True
    )

def add_arrow(x1, y1, x2, y2):
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(arrowstyle="->", lw=1.2)
    )

# --- Row 1 (top) ---
add_box(1, 6.2, 2.6, 1.2, "Transceiver\n(CAT Controlled)")
add_box(4.2, 6.2, 2.6, 1.2, "CAT Interface Layer\n(Serial or Hamlib/rigctld)")
add_arrow(3.6, 6.8, 4.2, 6.8)

# --- Row 2 (middle) — uniform height, more space ---
add_box(1, 3.8, 2.6, 1.6,
        "Perl Sweep Controller\n(Frequency Stepping\n& S‑meter Sampling)")
add_box(4.2, 3.8, 2.6, 1.6, "CSV Log Files")
add_arrow(3.6, 4.6, 4.2, 4.6)

# --- Row 3 (bottom) ---
add_box(2.6, 1.4, 2.8, 1.2,
        "Python Plotter\n(Panoramic & Timeseries Plots)")
add_arrow(5.0, 3.8, 3.8, 2.2)

# --- Save the diagram ---
output_path = r"C:\Radio\Python_Scripts\Scanner_block_diagram.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')

print(f"Diagram saved to: {output_path}")

plt.show()