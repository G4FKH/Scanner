# Scanner — HF Sweep Engine & Panoramic Plotting

Scanner is a CAT‑controlled HF sweep engine written in Perl, with Python tools for panoramic sweep plotting. It performs frequency sweeps, samples the rig’s dB value, and stores results as timestamped CSV files for later analysis.

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
│   ├── Figure3.png
│   └── Figure4.png
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

Scanner uses several Perl modules. Some are core modules, but others must be installed via CPAN.

Install required modules:

```bash
cpan install IO::Socket::INET Time::HiRes Win32::GUI Win32
```

### Python

- Python 3.x  
- pandas  
- matplotlib  

Install Python dependencies:

```bash
pip install pandas matplotlib
```

---

## Quick start

### 1. Run a sweep (Perl, GUI‑driven)

Start rigctld, e.g. rigctld -m 2039 -r COM1 -s 115200

Launch the sweep controller:

```bash
perl perl/scanner.pl
```

When the program starts, a GUI window prompts for:

- Start frequency  
- Stop frequency  
- Step size  

The script then controls the rig via CAT, samples the S‑meter, and writes a CSV file containing:

- Timestamp  
- Frequency  
- S‑meter reading  

Example output filename:

```
scan_2026-08-10_10-45-52.csv
```

### 2. Plot a sweep (Python)

```bash
python python/plot_sweep.py
```

The script automatically picks up the latest CSV file. This generates a panoramic sweep plot showing signal strength across the band.

---

## Example data

Example sweep CSVs are provided in `examples/`:

- `scan_2026-08-10_10-45-52.csv`

---

## Diagrams

Architecture diagrams are stored in `docs/`:

- `scanner_block_diagram.png`
- `scanner_hamlib_diagram.png`

---

## How the GUI Works

When you run `scanner.pl`, a GUI window appears prompting you for the sweep parameters:

- Start Frequency  
- Stop Frequency  
- Step Size  

These values define the sweep range and resolution.

### Sweep Process

Once you click **Proceed**:

1. The script controls the rig via CAT.  
2. Frequencies are stepped according to your chosen interval.  
3. The dB value is sampled at each step.  
4. Results are written to a timestamped CSV file.

Example output:

```
docs/2026-08-10_10-45-52.csv
```

---

## Troubleshooting CAT/COM Ports

CAT control depends on correct serial port configuration.  
If the sweep does not start or the rig does not respond, check the following:

### 1. Confirm the correct COM port

On Windows:

- Open **Device Manager**
- Expand **Ports (COM & LPT)**
- Identify the COM port used by your rig (e.g., `COM3`, `COM5`)
- Update the script or GUI settings accordingly

### 2. Check rig CAT settings

Ensure:

- CAT is enabled on the rig  
- Baud rate matches the script  
- Stop bits, parity, and flow control match your rig’s documentation  

### 3. Close other CAT applications

Only one program can access the COM port at a time. Close:

- Hamlib/rigctl  
- FLRig  
- WSJT‑X  
- Any logging software using CAT  

### 4. Permissions (Windows)

If the script cannot open the COM port:

- Run the terminal as **Administrator**  
- Ensure no antivirus is blocking Perl scripts  

### 5. Win32::SerialPort issues

If CPAN reports missing modules:

```bash
cpan install Win32::SerialPort
```

---

## Example Plot

Below is an example panoramic sweep plot generated using `plot_sweep.py`:

`[Looks like the result wasn't safe to show. Let's switch things up and try something else!]`

This plot shows signal strength across the band, with frequency on the x‑axis and S‑meter values on the y‑axis.

---

## Contributing

Contributions are welcome.  
The repository includes structured GitHub issue templates to help maintainers and users report problems or request enhancements.

### Issue Types

- **Bug Report**  
- **Feature Request**  
- **Data Issue**

### Pull Requests

1. Fork the repository  
2. Create a feature branch  
3. Commit changes with clear messages  
4. Submit a pull request describing the change  

### Code Style

- Perl: follow `strict` and `warnings` conventions  
- Python: PEP‑8 style preferred  
- Include comments for non‑obvious logic  
- Provide example data when relevant  

### Testing

Before submitting:

- Run a sweep using the GUI  
- Verify CSV output  
- Generate a plot using `plot_sweep.py`  
- Confirm no regressions in existing functionality  

---

## License

This project is released under the MIT license. You are free to use, modify, and extend the code for your own experiments.

---

## Contact

Gwyn, G4FKH  
Chelmsford, Essex

---

