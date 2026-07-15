# Scanner

README.md 

# HF Band Scanner – G4FKH

This repository contains the full source code for the HF band scanner described in my RadCom article.  
It includes the Perl sweep controller, Python plotting tools, example data, and the workflow used to generate the panoramic and time series figures.

The scanner performs a frequency sweep across a chosen HF band, samples the S meter at each step, logs the results to CSV, and produces publication quality plots.

---

## Contents

scanner/ 
│ 
├── perl/ 
│ └── sweep_controller.pl # CAT-controlled frequency sweep + S-meter sampling 
│ 
├── python/ │ 
├── plot_panoramic.py # Panoramic band plot (e.g., 80 m, 40 m) 
│ 
├── plot_timeseries.py # Time-series S-meter plot 
│ 
├── scanner_block_diagram.py # Figure 1 (system architecture) 
│ └── scanner_hamlib_diagram.py # Figure 4 (Hamlib compatibility) 
│ 
└── examples/ 
├── 80m_sweep.csv # Example sweep data 
└── 40m_sweep.csv # Example sweep data

---

## Requirements

### Perl
- Perl 5.x
- Install all the modules at the top of the .pl script with CPAN

### Other
- Hamlib (optional but recommended)
- rigctld (if using Hamlib CAT control), it comes with Hamlib

### Python
- Python 3.9+
- `matplotlib`
- `pandas`
- `numpy`

Install Python dependencies:

```bash
pip install matplotlib pandas numpy

Using the Sweep Controller
The sweep controller steps the transceiver across the band and samples the S meter at each frequency.

Serial CAT example:
bash
perl sweep_controller.pl --rig TS990 --start 3.500 --end 3.800 --step 0.25

Hamlib rigctld example:
Start rigctld:
bash
rigctld -m 204 -r /dev/ttyUSB0
Then run the sweep:
bash
perl sweep_controller.pl --hamlib localhost:4532 --start 7.000 --end 7.200 --step 0.25
The script produces a CSV file such as:
Code
2026-07-12_80m_sweep.csv

Plotting the Results
Panoramic plot:
bash
python plot_panoramic.py 2026-07-12_80m_sweep.csv

The repository includes the exact scripts used to generate Figures 2 and 3:
•	scanner_block_diagram.py – System architecture diagram
•	scanner_hamlib_diagram.py – Hamlib multi rig compatibility diagram
These produce high resolution PNG files for inclusion in the manuscript.

Notes for Experimenters
•	Sweep step size can be adjusted depending on band congestion.
•	The S meter sampling rate is intentionally conservative to avoid CAT overload.
•	Hamlib support allows the scanner to work with a wide range of rigs (TS 990S, IC 7300, FT 991A, IC 705, KX3, etc.).
•	Example CSV files are provided to help you test the plotting scripts without running a sweep.

License
This project is released under the MIT License. You are free to use, modify, and extend the code for your own experiments.

Contact
Gwyn, G4FKH 
Chelmsford, Essex
