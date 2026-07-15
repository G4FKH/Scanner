# HF Scanner System

A modular HF band‑scanner for CAT‑controlled frequency sweeps, S‑meter sampling, and panoramic/time‑series visualisation. Includes Perl sweep controller, Python analysis tools, and example datasets.

## Contents
```
scanner/
│
├── perl/
│   └── sweep_controller.pl        # CAT-controlled frequency sweep + S‑meter sampling
│
├── python/
│   ├── plot_panoramic.py          # Panoramic band plot (e.g., 80 m, 40 m)
│   ├── plot_timeseries.py         # Time-series S-meter plot
│   ├── scanner_block_diagram.py   # Figure 1 (system architecture)
│   └── scanner_hamlib_diagram.py  # Figure 4 (Hamlib compatibility)
│
└── examples/
├── 80m_sweep.csv              # Example sweep data
└── 40m_sweep.csv              # Example sweep data

```

## Overview

- CAT-controlled sweep across a defined HF band segment  
- S‑meter sampling at each frequency step  
- Output stored as CSV for downstream analysis  
- Python tools generate panoramic band plots and time‑series stability plots  
- Compatible with Hamlib‑supported radios

## Requirements

- Perl 5.x  
- Python 3.x  
- Hamlib (optional, for extended CAT support)  
- Matplotlib, Pandas (for plotting scripts)

## Usage

### 1. Run a sweep

perl sweep_controller.pl --start 3500 --stop 3800 --step 5 --radio IC7300
2. Generate panoramic plot
bash
python plot_panoramic.py examples/80m_sweep.csv
3. Generate time‑series plot
bash
python plot_timeseries.py examples/80m_sweep.csv
Notes
Sweep cadence and timing depend on radio CAT latency

CSV format is stable and suitable for external analysis

Figures are generated as PNG/SVG for publication use

## License
This project is released under the MIT License. You are free to use, modify, and extend the code for your own experiments.

## Contact
Gwyn, G4FKH 
Chelmsford, Essex
