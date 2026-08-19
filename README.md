# SeismicResilienceDEN: Full-cycle seismic resilience optimization of distributed energy networks

## Purpose

The code and data in this repository support the **peer review** of the manuscript:

**Spatiotemporal full-cycle optimal design enhances seismic resilience of distributed energy networks**

The materials are provided so that reviewers and future users can inspect the stochastic optimization workflow, run the released Harbin example, and examine the processed six-city source data used by the study.

The model represents a distributed energy network (DEN) under seismic disruption through a full-cycle **prevention–adaptation–restoration (PAR)** framework. It combines energy-system design, multi-energy operation, Monte Carlo earthquake sampling, component fragility, unmet demand, and post-hazard restoration in a Pyomo optimization model solved with Gurobi.

## Workflow overview

The released computational workflow is:

```text
Harbin model-ready input workbook
        ↓
Magnitude 6 / 7 / 8 earthquake annual occurrence probabilities
        ↓
Monte Carlo sampling of earthquake onset and component damage
        ↓
PAR optimization of design, operation, unmet demand, and restoration
        ↓
Gurobi solution for each stochastic realization
```

| Stage | Description |
|---|---|
| **Input data** | Harbin model-ready workbook containing inter-building distances, representative-week multiplicities, electricity/heating/cooling demand, energy prices, and solar-radiation profiles. |
| **Seismic settings** | Annual occurrence probabilities for magnitude 6, 7, and 8 earthquake scenarios, together with technology-specific fragility probabilities embedded in the notebook. |
| **Monte Carlo sampling** | Samples the earthquake onset time first and then samples component damage states for each stochastic realization. |
| **PAR optimization** | Co-optimizes system design and operation under seismic disruption, including unmet demand and restoration decisions. |
| **Model solution** | Solves the resulting Pyomo model with Gurobi for each Monte Carlo realization. |

## Data availability and public-release scope

The manuscript evaluates six Chinese cities: Beijing, Fuzhou, Harbin, Pu'er, Wuhan, and Xi'an. The executable public reproduction is provided for **Harbin**, while processed source data for all six cities are consolidated into a separate workbook.

| Material | Repository location | Scope |
|---|---|---|
| Full-cycle optimization notebook | `code/full_cycle_model.ipynb` | Harbin executable reproduction |
| Model-ready input workbook | `code/data/harbin_model_data.xlsx` | Harbin only; directly read by the notebook |
| Six-city supplementary source data | `data/six_city_supplementary_data.xlsx` | Beijing, Fuzhou, Harbin, Pu'er, Wuhan, and Xi'an |
| Python dependencies | `requirements.txt` | Public execution environment |

The six-city supplementary workbook is intended for source-data inspection. It contains the summer, transition-season, and winter representative-week electricity/heating/cooling loads, energy-price profiles, solar-radiation profiles, representative-week multiplicities, and city-level earthquake annual occurrence probabilities. It is **not** a replacement for the full model-ready Harbin workbook.

## Repository layout

```text
SeismicResilienceDEN/
├── README.md
├── requirements.txt
├── code/
│   ├── full_cycle_model.ipynb
│   └── data/
│       └── harbin_model_data.xlsx
└── data/
    └── six_city_supplementary_data.xlsx
```

## Python environment

Python **3.10 or later** is recommended. The released optimization is configured for **Gurobi 11.0** and requires a valid Gurobi license.

Create a virtual environment from the repository root:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux or macOS:

```bash
source .venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Harbin reproduction

Start Jupyter from the repository root:

```bash
jupyter lab
```

Open:

```text
code/full_cycle_model.ipynb
```

The user-facing Monte Carlo settings are defined at the beginning of the notebook:

```python
N_MONTE_CARLO = 1000
RANDOM_SEED = None
```

`N_MONTE_CARLO = 1000` reproduces the study-scale stochastic setting. A smaller value can be used for a quick functionality check. `RANDOM_SEED = None` retains stochastic sampling; an integer can be supplied when a repeatable debugging run is needed.

The notebook automatically locates:

```text
code/data/harbin_model_data.xlsx
```

No manual path editing is required when the repository structure is retained.

## Model configuration

The released Harbin model uses:

| Item | Setting |
|---|---|
| Representative buildings | 6 (`b1`–`b6`) |
| Time resolution | Hourly |
| Representative profile length | 168 h = 1 representative week |
| Climate conditions | Summer (`sum`), winter (`win`), transition season (`mid`) |
| Seismic conditions | Magnitude 6 (`M6`), magnitude 7 (`M7`), magnitude 8 (`M8`) earthquake scenarios |
| Monte Carlo realizations | 1000 by default |
| Optimization platform | Pyomo |
| Solver | Gurobi 11.0 |
| Solver MIP gap | 0.001 |
| Solver time limit | 2400 s per realization |

For model simplification, **based on local historical data, it is assumed that the seismic occurs in summer**. The earthquake scenarios are therefore evaluated under the summer representative condition. This assumption reduces the number of combined climate–seismic scenarios and the associated computational burden.

## Harbin model-ready input workbook

`code/data/harbin_model_data.xlsx` can be read directly by the released notebook. The original model sheet names are retained for compatibility; the workbook includes a `README` sheet with full descriptions and units.

| Model sheet | Full description | Unit / interpretation | Model role |
|---|---|---|---|
| `dist` | Inter-building distance matrix | Source unit not explicitly specified; `100000` denotes a prohibited connection / extremely large penalty distance | Network availability and pipe-investment calculations |
| `qty_day` | Representative-week multiplicity | weeks | Weights representative profiles in annual calculations |
| `e_dem` | Electricity demand | kW | Electricity-balance input |
| `c_dem` | Cooling demand | kW | Cooling-balance input |
| `h_dem` | Heating demand | kW | Heating-balance input |
| `price` | Grid purchase, grid feed-in, and natural-gas prices | CNY/kWh | Grid and fuel cost calculations |
| `SRI` | Solar radiation index | W/m² | PV-generation constraint |

The demand sheets use a two-level row index consisting of building (`b1`–`b6`) and model scenario (`sum`, `win`, `mid`, `M6`, `M7`, `M8`), followed by hourly columns `h1`–`h168`.

### Representative-week multiplicity

Each seasonal profile spans 168 hourly values. The `qty_day` values are therefore interpreted as **representative-week multiplicities**, rather than literal daily counts. For Harbin, the seasonal multiplicities are:

| Representative week | Model label | Multiplicity |
|---|---|---:|
| Summer | `sum` | 11 |
| Winter | `win` | 22 |
| Transition season | `mid` | 19 |

The three seasonal weights sum to 52 representative weeks.

## Six-city supplementary source data

`data/six_city_supplementary_data.xlsx` consolidates the processed source data for the six study cities into one formatted workbook. Full descriptive names and units are used in the tables; short model labels are retained only where needed to map the source data back to the executable model.

| Worksheet | Contents |
|---|---|
| `README` | Dataset scope, units, model-label definitions, and release notes |
| `Electricity_Load_kW` | Six-city summer, transition-season, and winter representative-week electricity demand |
| `Heating_Load_kW` | Six-city summer, transition-season, and winter representative-week heating demand |
| `Cooling_Load_kW` | Six-city summer, transition-season, and winter representative-week cooling demand |
| `Energy_Prices_CNY_per_kWh` | Grid-purchase, grid-feed-in, and natural-gas price profiles |
| `Solar_Radiation_W_per_m2` | Seasonal 168-hour solar-radiation profiles |
| `Seismic_Probabilities` | Magnitude 6 / 7 / 8 earthquake annual occurrence probabilities |
| `Representative_Week_Weights` | Summer, transition-season, and winter representative-week multiplicities |

All seasonal load and solar-radiation profiles contain **168 hourly values**, corresponding to one representative week.

## Seismic probability settings

`M6`, `M7`, and `M8` denote **magnitude 6 / 7 / 8 earthquake scenarios**. The values below are the **annual occurrence probabilities** used in the study.

| City | Magnitude 6 | Magnitude 7 | Magnitude 8 |
|---|---:|---:|---:|
| Beijing | 0.015274137 | 0.002311834 | 0.000349910 |
| Fuzhou | 0.006500000 | 0.000800000 | 0.000400000 |
| Harbin | 0.010600000 | 0.000100000 | 0.000030300 |
| Pu'er | 0.000222626 | 0.000037807 | 0.000007500 |
| Wuhan | 0.048260000 | 0.006817000 | 0.000960000 |
| Xi'an | 0.069747010 | 0.011575122 | 0.001920992 |

The Supplementary Information describes the upstream location-specific seismic probability model using CPSHA, a truncated Gutenberg–Richter magnitude distribution, a Poisson occurrence model, and peak ground acceleration as a function of magnitude and epicentral distance. The public notebook uses the resulting city-level annual occurrence probabilities as model inputs.

## Energy-system components

The Pyomo formulation includes:

| Component | Model representation |
|---|---|
| Combined heat and power | Capacity, electricity/heat production, part-load and startup constraints, seismic damage and restoration |
| Boiler | Heating capacity and production, fuel consumption, seismic damage and restoration |
| Electric chiller | Cooling capacity, electricity consumption, seismic damage and restoration |
| Absorption chiller | Cooling capacity, heat consumption, seismic damage and restoration |
| Heat pump | Heating capacity, electricity consumption, seismic damage and restoration |
| Electrical storage | Capacity, charging/discharging, stored energy, seismic damage and restoration |
| Cooling storage | Capacity, charging/discharging, stored cooling, seismic damage and restoration |
| Photovoltaics | Installed area and solar-radiation-dependent output, seismic damage and restoration |
| Utility grid | Electricity import/export and seismic availability |
| Heating/cooling networks | Inter-building transfer, pipe selection, transfer losses, seismic damage and restoration |

## Seismic damage and restoration treatment

For each Monte Carlo realization, the model first samples an earthquake onset hour and then samples component damage according to the magnitude-specific fragility probabilities.

The restoration thresholds implemented in the notebook include both the **preparation/logistical delay** and the **component restoration time**. The restoration-time values reported in the manuscript and Supplementary Information refer to the component restoration duration itself; the code thresholds therefore occur later than those tabulated restoration durations.

## Model outputs

The public notebook is intended to demonstrate model solution rather than generate a separate result-export package. After each feasible Gurobi solve, it reports basic values including:

- total annualized objective value;
- unmet-demand cost (UDC);
- expected energy not supplied (EENS);
- restoration cost.

All Pyomo decision variables remain available in the solved model instance for inspection. The unused EIU calculation and the former large in-memory result-collection containers are not included in the public release.

## Replication notes

Before running the model, confirm that:

1. `code/data/harbin_model_data.xlsx` remains in its released location and its model sheet names are unchanged;
2. the notebook is run with a valid Gurobi 11.0 license;
3. a smaller `N_MONTE_CARLO` value is used for a quick test before launching the default 1000-realization calculation;
4. `M6`, `M7`, and `M8` are interpreted as magnitude 6, 7, and 8 earthquake scenarios, with the supplied values representing annual occurrence probabilities;
5. the seismic cases use the summer representative condition under the study's simplifying assumption;
6. `100000` in the distance matrix is retained as the prohibited-connection / extreme-penalty value;
7. the six-city supplementary workbook is treated as processed source data and not as a direct substitute for the Harbin model-ready workbook.

## Status

- The full-cycle Pyomo/Gurobi model notebook is included.
- A directly executable Harbin model-input workbook is included.
- Processed six-city seasonal load, energy-price, solar-radiation, seismic-probability, and representative-week data are included in one supplementary workbook.
- The public code uses Python 3.10 or later and Gurobi 11.0.
- No separate result-export package is required for the released reproduction.
