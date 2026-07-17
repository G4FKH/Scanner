# HF Scanner System

A modular HF band‑scanner for CAT‑controlled frequency sweeps, S‑meter sampling, and panoramic/time‑series visualisation. Includes Perl sweep controller, Python analysis tools, and example datasets.

## Contents
```
scanner/
│
├── perl/
│   └── scanner.pl                 # CAT-controlled frequency sweep + S‑meter sampling
│
├── python/
│   ├── plot_sweep.py              # Panoramic band plot (e.g., 80 m, 40 m)
│   ├── scanner_block_diagram.py   # Figure 1 (system architecture)
│   └── scanner_hamlib_diagram.py  # Figure 4 (Hamlib compatibility)
│
└── examples/
├── 80m_sweep.csv                  # Example sweep data
└── 40m_sweep.csv                  # Example sweep data

```

## Overview

- CAT-controlled sweep across a defined HF band segment  
- S‑meter sampling at each frequency step  
- Output stored as CSV for downstream analysis  
- Python tools generate panoramic band plots  
- Compatible with Hamlib‑supported radios

## Requirements

- Perl 5.x  
- Python 3.x  
- Hamlib (optional, for extended CAT support)  
- Matplotlib, Pandas (for plotting scripts)

## Technical Specification

### 1. System Architecture
- Modular HF scanning system comprising:
  - CAT‑controlled sweep engine (Perl)
  - Data acquisition and CSV logging
  - Python‑based analysis and visualisation modules
- Operates on standard HF transceivers supporting CAT commands (Kenwood, Icom, Yaesu, via Hamlib or native CAT).

### 2. Sweep Controller (Perl)
- Frequency stepping:
  - User‑defined start/stop frequencies (Hz)
  - Fixed step size (Hz)
  - Optional dwell time per step
- Radio control:
  - CAT commands issued over serial/USB
  - Hamlib optional for extended device support
- Measurement:
  - S‑meter sampling at each frequency step
  - Timestamped acquisition
- Output:
  - CSV file containing: frequency, S‑meter value, timestamp

### 3. Data Format (CSV)
- Columns:
  - `freq_hz` — tuned frequency (Hz)
  - `s_meter` — raw or normalised S‑meter reading
  - `timestamp` — ISO‑8601 UTC timestamp
- Guaranteed stable schema for downstream processing.

### 4. Python Analysis Modules
#### plot_sweep.py
- Generates panoramic band‑sweep plots.
- Features:
  - Frequency‑domain visualisation
  - Optional smoothing or median filtering
  - PNG/SVG output

#### scanner_block_diagram.py / scanner_hamlib_diagram.py
- Generates architecture and compatibility diagrams.
- Output formats: PNG/SVG.

### 5. Performance Characteristics
- Sweep rate determined by:
  - CAT command latency
  - Radio tuning speed
  - Step size and dwell time
- Typical sweep cadence:
  - 3–5 seconds per full HF band segment (radio‑dependent)
- Data throughput:
  - ~100–500 samples per sweep depending on configuration.

### 6. Dependencies
- Perl 5.x
- Python 3.x
- Hamlib (optional)
- Python libraries:
  - `matplotlib`
  - `pandas`
  - `numpy` (optional)
-  Perl Modules
  - use CPAN to install all modules at the top of the script

### 7. Operating Environment
- Tested on:
  - Linux (Debian/Ubuntu)
  - macOS
  - Windows (with appropriate serial drivers)
- Requires stable CAT connection (USB/serial).

### 8. Limitations
- Sweep accuracy limited by radio CAT tuning resolution.
- S‑meter readings are radio‑specific and not calibrated in dBm.
- High sweep rates may cause CAT buffer overruns on older radios.

### 9. File Outputs
- CSV data files (primary)
- PNG/SVG figures (secondary)
- Optional logs for debugging CAT communication.


## Usage

### 10. Run a sweep

1. NB: rigctld must be started prior to running the scanner.pl script.

   E.G. from a command prompt - rigctld -m 2039 -r COM1 -s 115200
   
   scanner.pl

   Close the command prompt with CNTL-C

3. Generate panoramic plot

python plot_sweep.py (examples/80m_sweep.csv)

Notes:
Sweep cadence and timing depend on radio CAT latency

CSV format is stable and suitable for external analysis

Figures are generated as PNG/SVG for publication use

## License
This project is released under the MIT License. You are free to use, modify, and extend the code for your own experiments.

## Contact
Gwyn, G4FKH 
Chelmsford, Essex
