# Smart Irrigation System Using Sugeno Fuzzy Logic

A Python-based, software-only mini-project that estimates irrigation duration from soil moisture and temperature using a zero-order Sugeno Fuzzy Inference System.

## Features
- Soil moisture input: 0–100%
- Temperature input: 0–50°C
- Triangular membership functions with shoulder sets at boundaries
- Nine zero-order Sugeno rules (3 soil-moisture sets × 3 temperature sets)
- Minimum operator for the AND condition
- Weighted-average Sugeno output
- Streamlit dashboard, rule trace, membership plots, and response surface
- Predefined sample scenarios

## Requirements
- Python 3.10 or newer recommended
- pip

## Setup

```bash
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows Command Prompt**
```bat
.venv\Scripts\activate.bat
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the application

```bash
streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`. Open that URL in your browser.

## Run basic tests

```bash
python test_cases.py
```

## Model design

### Inputs
- Soil moisture: 0–100%
- Temperature: 0–50°C

### Membership functions
Soil moisture:
- Low: (0, 0, 40)
- Medium: (20, 50, 80)
- High: (60, 100, 100)

Temperature:
- Low: (0, 0, 20)
- Medium: (10, 25, 40)
- High: (30, 50, 50)

The triplets are (a, b, c) for triangular membership functions. Repeated endpoints create left/right shoulder functions.

### Zero-order Sugeno consequents

| Soil moisture | Low temperature | Medium temperature | High temperature |
|---|---:|---:|---:|
| Low | 7 min | 8 min | 10 min |
| Medium | 3 min | 4 min | 6 min |
| High | 0 min | 0 min | 0 min |

These values are illustrative for a learning project and are not validated agricultural recommendations.

### Inference
For each rule, the firing strength is the minimum of the two antecedent membership degrees:

`w_i = min(mu_soil, mu_temperature)`

The final output is:

`duration = sum(w_i * z_i) / sum(w_i)`

where `z_i` is the constant output for rule `i`.

## Project structure

```text
smart_irrigation_sugeno/
├── app.py
├── membership.py
├── sugeno.py
├── visualizations.py
├── test_cases.py
├── requirements.txt
└── README.md
```

## Limitations
This project is a simulation. It does not connect to sensors, control a pump, or account for crop type, soil type, rainfall, root depth, flow rate, or evapotranspiration. Real-world use requires agronomic validation and safety controls.
