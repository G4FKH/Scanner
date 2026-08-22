import os
import glob
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from matplotlib.ticker import FormatStrFormatter

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
BASE_DIR = r"C:\Radio\Perl_Apps\Scanner"
ARCHIVE_DIR = os.path.join(BASE_DIR, "Archive")

os.makedirs(ARCHIVE_DIR, exist_ok=True)

# ------------------------------------------------------------
# Find latest CSV file
# ------------------------------------------------------------
csv_files = glob.glob(os.path.join(BASE_DIR, "scan_*.csv"))
if not csv_files:
    print("No CSV files found in Scanner directory.")
    exit(1)

latest_csv = max(csv_files, key=os.path.getmtime)
print(f"Using CSV file: {latest_csv}")

# ------------------------------------------------------------
# Load CSV (comma-separated)
# ------------------------------------------------------------
df = pd.read_csv(latest_csv, sep=",", header=0)

# Normalise column names
df.columns = [c.strip().lower() for c in df.columns]

# Expected columns
freq_col = "freq_hz"
s_col = "s_meter"
time_col = "timestamp"

# Convert frequency to MHz
df["freq_mhz"] = df[freq_col] / 1_000_000.0

# ------------------------------------------------------------
# AUTO-DETECT STEP SIZE (Hz)
# ------------------------------------------------------------
freqs = df["freq_mhz"].values
if len(freqs) > 1:
    step_hz = int(round(abs(freqs[1] - freqs[0]) * 1_000_000))
else:
    step_hz = None

# Extract start/end timestamps for title
start_time = str(df[time_col].iloc[0])
end_time = str(df[time_col].iloc[-1])

title_text = f"Scan for {start_time} – {end_time}"

# ------------------------------------------------------------
# Plotting
# ------------------------------------------------------------
plt.figure(figsize=(12, 6))

# Left axis: raw S-meter values (in dB-like units)
ax = plt.gca()
ax.plot(df["freq_mhz"], df[s_col], color="blue", linewidth=1)
ax.xaxis.set_major_formatter(FormatStrFormatter('%.3f'))

ax.set_xlabel("Frequency (MHz)")
ax.set_ylabel("Signal Strength (dB)")

# ------------------------------------------------------------
# Right axis: S-units based on your measured calibration
# ------------------------------------------------------------
ax2 = ax.twinx()
ax2.set_ylabel("S-units")

# Your measured anchor points
s_cal = {
    1: -50,
    3: -46,
    5: -40,
    7: -33,
    9: -27,
    10: -17,   # S9+10
}

# Full S scale: S1–S9 plus S9+10
s_units  = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
s_values = np.interp(s_units, list(s_cal.keys()), list(s_cal.values()))
s_labels = ["S1","S2","S3","S4","S5","S6","S7","S8","S9","S9+10"]

ax2.set_yticks(s_values)
ax2.set_yticklabels(s_labels)

# ------------------------------------------------------------
# Noise floor estimation (quietest 10% of samples)
# ------------------------------------------------------------
noise_floor = df[s_col].quantile(0.10)   # 10th percentile

# Draw horizontal noise-floor line
ax.axhline(noise_floor, color="red", linestyle="--", linewidth=1)

# Label it on the left axis
ax.text(
    df["freq_mhz"].min(),
    noise_floor - 0.3,     # move below the line
    f"Noise floor = {noise_floor:.1f} dB",
    color="red",
    fontsize=9,
    va="top",              # anchor from above
    ha="left"
)

ax.fill_between(
    df["freq_mhz"],
    ax.get_ylim()[0],
    noise_floor,
    color="red",
    alpha=0.10
)

# ------------------------------------------------------------
# Shaded region below the noise floor
# ------------------------------------------------------------
ax.fill_between(
    df["freq_mhz"],
    ax.get_ylim()[0],      # bottom of the plot
    noise_floor,
    color="red",
    alpha=0.10
)

# IMPORTANT:
# Do NOT force ax.set_ylim() — let Matplotlib auto-scale the left axis
# This restores the original look of your sweep plots.

plt.title(title_text)
plt.grid(True, linestyle="--", alpha=0.4)

# Add annotation box for step size
plt.text(
    0.98, 0.98,
    "Generated from data gathered in 250 Hz steps",
    transform=plt.gca().transAxes,
    fontsize=9,
    ha='right', va='top',
    bbox=dict(facecolor='white', edgecolor='black', alpha=0.7)
)

png_name = f"sweep_{start_time.replace(':','').replace('-','').replace(' ','_')}.png"
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, png_name))
plt.close()

print(f"Graph saved as {png_name}")

# ------------------------------------------------------------
# Move CSV to Archive
# ------------------------------------------------------------
dest_csv = os.path.join(ARCHIVE_DIR, os.path.basename(latest_csv))
shutil.move(latest_csv, dest_csv)
print(f"Moved CSV to archive: {dest_csv}")

# ------------------------------------------------------------
# Clean archive (older than 7 days)
# ------------------------------------------------------------
now = datetime.now()
deleted = 0

for f in glob.glob(os.path.join(ARCHIVE_DIR, "*.csv")):
    mtime = datetime.fromtimestamp(os.path.getmtime(f))
    if now - mtime > timedelta(days=7):
        os.remove(f)
        deleted += 1

print(f"Archive cleanup complete. Deleted {deleted} old file(s).")
print("Plotting complete.")