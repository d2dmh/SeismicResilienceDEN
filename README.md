# Full-cycle seismic resilience optimization of distributed energy networks

This repository provides the organized research code and six-city input dataset for a distributed energy network (DEN) seismic-resilience study. The model integrates **pre-hazard prevention, in-hazard adaptation, and post-hazard restoration (PAR)** in a stochastic multi-energy optimization framework.

The public package is organized so that a reader can identify the model entry point, understand every input workbook, select a city, and trace the main variables and outputs without needing the authors' original working folders.

## What is included

- one cleaned and documented Pyomo/Gurobi model notebook;
- six city-specific Excel input workbooks;
- one readable seismic-probability configuration table;
- a data manifest and field-level data dictionary;
- model-formulation notes mapped to the current manuscript and Supplementary Information;
- reproducibility instructions and repository integrity tests.

## Repository structure

```text
SeismicResilienceDEN/
├── README.md
├── requirements.txt
├── CITATION.cff
├── .gitignore
├── code/
│   ├── README.md
│   └── full_cycle_model.ipynb
├── config/
│   ├── README.md
│   └── seismic_probabilities.csv
├── data/
│   ├── README.md
│   ├── DATA_MANIFEST.csv
│   ├── beijing/model_data.xlsx
│   ├── fuzhou/model_data.xlsx
│   ├── harbin/model_data.xlsx
│   ├── puer/model_data.xlsx
│   ├── wuhan/model_data.xlsx
│   └── xian/model_data.xlsx
├── docs/
│   ├── DATA_DICTIONARY.md
│   ├── MODEL_DESCRIPTION.md
│   └── REPRODUCTION.md
├── results/
│   └── README.md
└── tests/
    └── test_repository_integrity.py
```

## Study cases

The current dataset contains six representative urban districts spanning northern/southern climatic conditions and high/medium/low seismic-risk groups.

| City | Climate group | Seismic-risk group | M6 | M7 | M8 |
|---|---|---|---:|---:|---:|
| Beijing | North | Medium | 0.015274137 | 0.002311834 | 0.000349910 |
| Fuzhou | South | Medium | 0.006500000 | 0.000800000 | 0.000400000 |
| Harbin | North | Low | 0.010600000 | 0.000100000 | 0.000030300 |
| Pu'er | South | Low | 0.000222626 | 0.000037807 | 0.000007500 |
| Wuhan | South | High | 0.048260000 | 0.006817000 | 0.000960000 |
| Xi'an | North | High | 0.069747010 | 0.011575122 | 0.001920992 |

`M6`, `M7`, and `M8` are the city-level annual seismic occurrence probabilities supplied with the research materials. The updated Supplementary Information describes the CPSHA procedure used to derive magnitude-bin probabilities and PGA from the GB18306-2015 China Seismic Parameter Zoning Map. The complete regional parameter set needed to regenerate the six numeric probability triplets is not included here, so the supplied values are treated as model inputs rather than recalculated.

## Computational workflow

```text
City workbook
  ├─ dist       building-to-building distance matrix
  ├─ qty_day    representative-period multiplicity
  ├─ e_dem      electricity demand
  ├─ c_dem      cooling demand
  ├─ h_dem      heating demand
  ├─ price      grid and natural-gas prices
  └─ SRI        solar radiation index
          │
          ├──────── config/seismic_probabilities.csv
          │          M6/M7/M8 annual occurrence probabilities
          ↓
Pyomo full-cycle DEN model
  ├─ technology sizing
  ├─ electricity / heating / cooling balances
  ├─ storage and network operation
  ├─ Monte Carlo earthquake onset
  ├─ component fragility and damage states
  ├─ unmet demand and EENS
  └─ repair / restoration decisions
          ↓
Gurobi optimization for each Monte Carlo realization
          ↓
in-memory result containers (`m.ag_*`)
```

## Quick start

Python 3.10+ is recommended.

```bash
python -m venv .venv
```

Activate the environment and install dependencies:

```bash
pip install -r requirements.txt
```

A local **Gurobi installation and valid Gurobi license** are required.

Start Jupyter from the repository root:

```bash
jupyter lab
```

Open:

```text
code/full_cycle_model.ipynb
```

The first configuration cell contains the user-facing controls:

```python
CITY = "harbin"      # beijing | fuzhou | harbin | puer | wuhan | xian
N_MONTE_CARLO = 1000
RANDOM_SEED = None
```

`RANDOM_SEED = None` preserves stochastic sampling. Set an integer only when a repeatable realization is required for debugging or benchmarking.

## Input workbook structure

Every city workbook has the same seven worksheets:

| Sheet | Shape including headers | Main role |
|---|---:|---|
| `dist` | 7 × 7 | 6×6 pairwise building-distance matrix |
| `qty_day` | 7 × 7 | representative-period multiplicities for `sum`, `win`, `mid`, `M6`, `M7`, `M8` |
| `e_dem` | 37 × 170 | electricity demand: 6 buildings × 6 scenarios × 168 hourly values |
| `c_dem` | 37 × 170 | cooling demand: 6 buildings × 6 scenarios × 168 hourly values |
| `h_dem` | 37 × 170 | heating demand: 6 buildings × 6 scenarios × 168 hourly values |
| `price` | 5 × 169 | 168-hour price profiles for `grid_buy1`, `grid_buy2`, `grid_sell`, `NG` |
| `SRI` | 7 × 169 | 168-hour solar radiation profiles for the six scenarios |

See [`data/README.md`](data/README.md) for a file-by-file explanation and [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md) for field-level definitions, model mappings, and unit notes.

## Model scope

The current implementation includes:

- six representative buildings (`b1`–`b6`);
- 168 hourly time steps per representative profile (`h1`–`h168`);
- climate conditions `sum`, `win`, and `mid`;
- seismic conditions `M6`, `M7`, and `M8`;
- CHP, boiler, electric chiller, absorption chiller, heat pump, battery, cooling storage, grid, PV, and heating/cooling networks;
- technology-specific fragility probabilities;
- stochastic earthquake onset within hours 1–24;
- unmet electricity/heating/cooling demand;
- restoration decisions and restoration costs;
- total annualized cost, EENS, EIU, capacity, dispatch, and cost-component results.

The objective implemented in the notebook combines device and pipe capital cost, fuel cost, maintenance cost, grid purchase minus grid-sale revenue, unmet-demand cost, and restoration cost. A detailed equation-to-code summary is provided in [`docs/MODEL_DESCRIPTION.md`](docs/MODEL_DESCRIPTION.md).

## Output behavior

The supplied model does not automatically write a final CSV/Excel result package. During the Monte Carlo loop, results are copied into Pyomo mutable parameters named `m.ag_*`, including:

- total objective (`ag_results`);
- disaster/unmet-demand cost;
- device and pipe cost;
- maintenance and fuel cost;
- grid import/export cost;
- restoration cost;
- EENS and EIU;
- technology capacities;
- hourly dispatch and inter-building flows;
- damage-hour and restoration-related values.

The `results/` directory is intentionally empty in the repository and is reserved for future exported outputs.

## Source and documentation boundary

The current Supplementary Information now documents the DES cost objective, the base mathematical constraints, and the location-specific seismic probability model. However, its subsection labelled seismic constraints is still incomplete in the supplied version. For the actual implemented seismic damage/restoration logic, the public notebook is therefore the authoritative computational source in this package. Details and specific paper/code discrepancies are documented in [`docs/MODEL_DESCRIPTION.md`](docs/MODEL_DESCRIPTION.md).

## Repository integrity check

Run:

```bash
python -m unittest discover -s tests -v
```

The tests verify file organization, six-city probability values, workbook sheet names, notebook syntax, and required documentation. They do **not** solve the optimization model.

## Citation

See `CITATION.cff`. Update the final journal citation and DOI when the associated manuscript is publicly available.

## License

No software/data license was specified in the supplied research materials. A license should be selected by the project authors before formal public release.
