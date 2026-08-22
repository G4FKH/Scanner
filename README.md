# Scanner — HF Sweep Engine & Panoramic Plotting

Scanner is a CAT‑controlled HF sweep engine written in Perl, with Python tools for panoramic sweep plotting. It performs frequency sweeps, samples the rig’s S‑meter, and stores results as timestamped CSV files for later analysis.

---

## Features

- CAT‑controlled HF sweep engine (`perl/scanner.pl`)
- GUI input for sweep parameters (start/stop frequency, step size)
- Timestamped CSV logging with S‑meter sampling
- Python panoramic sweep plotting (`python/plot_sweep.py`)
- Architecture diagrams (`docs/`)
- Example sweep datasets (`examples/`)
- MIT‑licensed

---

## Repository structure

```text
scanner/
│
├── perl/
│   └── scanner.pl
│
├── python/
│   ├── plot_sweep.py
│   └── scanner_block_diagram.py
│
├── examples/
│   ├── 80m_sweep.csv
│   └── 40m_sweep.csv
│
├── docs/
│   ├── scanner_block_diagram.png
│   └── scanner_hamlib_diagram.png
│
├── README.md
├── LICENSE
├── CHANGELOG.md
└── VERSION
```

---

## Requirements

### Perl
- Perl 5.x  
- Hamlib (optional, for rig control)
### Perl modules

Scanner uses several Perl modules which may not be installed by default.  
Use CPAN to install any missing modules:

```bash
cpan install Tk Time::HiRes IO::Socket::INET Time::HiRes qw(usleep) POSIX qw(strftime) IO::Handle Cwd Win32 Win32::GUI;
```

### Python
- Python 3.x  
- pandas  
- matplotlib

Install Python dependencies:

```bash
pip install pandas matplotlib
```




