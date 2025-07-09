# utils/plot_helper.py
import os
import matplotlib.pyplot as plt

def save_plot(fig, filename, subfolder="charts"):
    output_dir = os.path.join("outputs", subfolder)
    os.makedirs(output_dir, exist_ok=True)
    fig.savefig(os.path.join(output_dir, filename), dpi=300, bbox_inches="tight")
    print(f"📁 Chart saved to outputs/{subfolder}/{filename}")
