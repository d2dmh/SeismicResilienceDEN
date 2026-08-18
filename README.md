# SeismicResilienceDEN: Full-cycle seismic resilience of distributed energy networks

## Purpose

The code and data in this repository support the **peer review** of the manuscript:

**Spatiotemporal full-cycle optimal design enhances seismic resilience of distributed energy networks**

The materials are provided so that reviewers and future users can inspect the stochastic optimization framework, reproduce the released six-city model inputs, and examine how seismic risk, component damage, energy-system operation, and restoration are coupled in the distributed energy network (DEN) model.

The released implementation uses **Pyomo** for mathematical optimization and **Gurobi** as the solver. It represents the full **Prevention–Adaptation–Restoration (PAR)** cycle: pre-hazard system design, in-hazard redispatch under component failures, and post-hazard restoration.

## Workflow overview

The released computational workflow is:

```text
Six-city demand, price, solar-radiation, and network inputs
        ↓
City-specific seismic occurrence probabilities (M6 / M7 / M8)
        ↓
Monte Carlo sampling of earthquake onset and component damage
        ↓
Full-cycle DEN optimization
  ├─ Prevention: capacity and network design
  ├─ Adaptation: post-damage multi-energy redispatch
  └─ Restoration: repair decisions and restoration cost
        ↓
System cost, unmet demand, EENS / EIU, capacities, dispatch, and restoration results
```

| Stage | Description |
|---|---|
| **Input data** | Six city-specific workbooks containing electricity, heating and cooling demand, energy prices, solar-radiation inputs, representative-period multiplicities, and inter-building distances. |
| **Seismic setting** | Annual occurrence probabilities for the model scenarios labelled `M6`, `M7`, and `M8`, together with technology-specific failure probabilities embedded in the notebook. |
| **Monte Carlo sampling** | Samples earthquake onset time and component damage states for each realization. |
| **PAR optimization** | Co-optimizes energy-system design, post-hazard operation, unmet demand, and restoration within the implemented Pyomo formulation. |
| **Result collection** | Stores objective, cost, resilience, capacity, dispatch, flow, damage, and restoration quantities in `m.ag_*` result containers. |

## Data availability and public-release scope

The study contains six representative urban districts: **Beijing, Fuzhou, Harbin, Pu'er, Wuhan, and Xi'an**. The model workbook for all six cities is included in this repository.

| Material | Public location | Scope |
|---|---|---|
| Full-cycle optimization notebook | `code/full_cycle_model.ipynb` | Six-city model; select one city at a time |
| City seismic-probability configuration | `code/config/seismic_probabilities.csv` | Six cities |
| City model workbooks | `data/<city>/model_data.xlsx` | Six cities |
| Python dependencies | `requirements.txt` | Pyomo/Gurobi environment |
| Final exported benchmark-result package | Not currently included | To be added after author-side numerical validation |
| Manuscript figure source data | Not currently included | Outside the present code-and-input release |

The repository contains the input workbooks required by the released notebook. A local Gurobi installation and valid Gurobi license are required to solve the optimization model.

## Repository layout

```text
SeismicResilienceDEN/
├── README.md
├── requirements.txt
├── code/
│   ├── full_cycle_model.ipynb
│   └── config/
│       └── seismic_probabilities.csv
└── data/
    ├── beijing/
    │   └── model_data.xlsx
    ├── fuzhou/
    │   └── model_data.xlsx
    ├── harbin/
    │   └── model_data.xlsx
    ├── puer/
    │   └── model_data.xlsx
    ├── wuhan/
    │   └── model_data.xlsx
    └── xian/
        └── model_data.xlsx
```

## Python environment

Python 3.10 or later is recommended.

Create and activate a virtual environment from the repository root:

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

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

The principal dependencies are:

```text
numpy>=1.24,<3
pandas>=2.0,<3
openpyxl>=3.1,<4
pyomo>=6.7,<7
gurobipy>=11,<13
jupyterlab>=4,<5
```

A valid **Gurobi license** is required.

## Running the model

Start Jupyter from the repository root:

```bash
jupyter lab
```

Open:

```text
code/full_cycle_model.ipynb
```

The first configuration cell contains the user-facing settings:

```python
CITY = "harbin"      # beijing | fuzhou | harbin | puer | wuhan | xian
N_MONTE_CARLO = 1000
RANDOM_SEED = None
```

The notebook reads the selected city workbook and city-level seismic probabilities automatically from the repository-relative paths.

For a short functionality check, reduce `N_MONTE_CARLO` before running the notebook. The full study-scale setting uses `N_MONTE_CARLO = 1000` and can be computationally expensive because Gurobi solves one large optimization problem for each realization.

`RANDOM_SEED = None` preserves stochastic sampling between runs. An integer can be supplied for a repeatable debugging or benchmark run.

## Input data

Each city workbook contains the same seven worksheets. The numerical workbook structure is retained across all six cases.

| Sheet | Structure | Model role |
|---|---|---|
| `dist` | 6 × 6 building-to-building matrix (`b1`–`b6`) | Inter-building distance used in heating/cooling network investment and transfer calculations |
| `qty_day` | 6 buildings × 6 conditions | Multiplicity used when annualizing representative 168-hour profiles |
| `e_dem` | building × condition × `h1`–`h168` | Electricity demand |
| `c_dem` | building × condition × `h1`–`h168` | Cooling demand |
| `h_dem` | building × condition × `h1`–`h168` | Heating demand |
| `price` | 4 price series × `h1`–`h168` | Grid-purchase, grid-sale, and natural-gas prices |
| `SRI` | 6 conditions × `h1`–`h168` | Solar radiation index used by the PV formulation |

### `dist`

The rows and columns are `b1`–`b6`. The matrix is read as `m.dist[i, j]` and enters pipe/network calculations.

The supplied workbook does not explicitly label the distance unit. The implemented pipe-loss parameters are expressed per 1000 m, so metres are the working interpretation pending final author confirmation. Several entries use the value `100000`; this value is retained exactly as supplied.

### `qty_day`

Columns are:

```text
sum, win, mid, M6, M7, M8
```

The notebook reads these values as `m.qty_day[s, i]`. Each demand/price/SRI profile contains 168 hourly values (7 × 24 h), and `qty_day` is used as a multiplicity in annualized cost and demand-loss calculations. The repository retains the original field name because the precise terminology for this weighting quantity should be confirmed by the model authors.

### `e_dem`, `c_dem`, and `h_dem`

These worksheets use a two-level row index:

```text
building:  b1 ... b6
condition: sum, win, mid, M6, M7, M8
```

with hourly columns:

```text
h1 ... h168
```

They are mapped to:

```text
e_dem → m.e_demand[i, s, h]
c_dem → m.c_demand[i, s, h]
h_dem → m.h_demand[i, s, h]
```

The supplied workbook headers do not explicitly state the energy/load unit, so no unit is added here by assumption.

### `price`

The four rows are:

| Row | Model use |
|---|---|
| `grid_buy1` | Grid-purchase tariff applied to `b1`–`b5` |
| `grid_buy2` | Grid-purchase tariff applied to `b6` |
| `grid_sell` | Electricity export/feed-in tariff |
| `NG` | Natural-gas price used by CHP and boiler fuel-cost terms |

All rows contain `h1`–`h168`. The supplied workbook does not explicitly state the monetary/energy unit.

### `SRI`

Rows are `sum`, `win`, `mid`, `M6`, `M7`, and `M8`; columns are `h1`–`h168`.

The Supplementary Information defines SRI in **W/m²**. The notebook maps the sheet to `m.SRI[s, h]` and uses it in the PV-generation constraint.

## Seismic probability settings

The city-level configuration is stored in:

```text
code/config/seismic_probabilities.csv
```

| City | Climate group | Seismic-risk group | M6 | M7 | M8 |
|---|---|---|---:|---:|---:|
| Beijing | North | Medium | 0.015274137 | 0.002311834 | 0.000349910 |
| Fuzhou | South | Medium | 0.006500000 | 0.000800000 | 0.000400000 |
| Harbin | North | Low | 0.010600000 | 0.000100000 | 0.000030300 |
| Pu'er | South | Low | 0.000222626 | 0.000037807 | 0.000007500 |
| Wuhan | South | High | 0.048260000 | 0.006817000 | 0.000960000 |
| Xi'an | North | High | 0.069747010 | 0.011575122 | 0.001920992 |

The values above are the annual occurrence probabilities supplied with the model materials for the three seismic scenarios labelled `M6`, `M7`, and `M8`.

The Supplementary Information describes the upstream location-specific seismic probability model using China Probabilistic Seismic Hazard Analysis (CPSHA), the GB18306-2015 China Seismic Parameter Zoning Map, a truncated Gutenberg–Richter magnitude distribution, a Poisson occurrence model, and peak ground acceleration (PGA) as a function of magnitude and epicentral distance. The regional coefficients required to independently regenerate every city-specific probability value are not included in the present repository, so the supplied probabilities are treated as model inputs.

## Model settings

| Setting | Released implementation |
|---|---|
| Buildings | 6 representative buildings (`b1`–`b6`) |
| Hourly profile | 168 h (`h1`–`h168`) |
| Non-seismic conditions | `sum`, `win`, `mid` |
| Seismic conditions | `M6`, `M7`, `M8` |
| Monte Carlo realizations | 1000 by default |
| Earthquake onset sampling | Integer hour sampled from 1–24 |
| Energy carriers | Electricity, heating, cooling |
| Solver | Gurobi |
| MIP gap | 0.001 |
| Time limit | 2400 s per realization |

The technology set includes:

```text
CHP
boiler
electric chiller
absorption chiller
heat pump
electrical storage
cooling storage
PV
utility grid
heating network
cooling network
```

The objective minimizes total annualized system cost, including device and pipe capital cost, fuel cost, maintenance cost, grid-purchase cost minus grid-sale revenue, unmet-demand cost, and restoration cost.

## Outputs

The current notebook collects successful Monte Carlo solutions into mutable Pyomo result containers with the prefix `m.ag_*`.

Principal result groups include:

| Result group | Examples |
|---|---|
| Total and component costs | `ag_results`, `ag_Disaster_cost`, `ag_device_cost`, `ag_pipe_cost`, `ag_maint_cost`, `ag_fuel_cost`, `ag_grid_im_cost`, `ag_grid_ex_cost`, `ag_restored_cost` |
| Resilience metrics | `ag_EENS`, `ag_EIU` |
| Optimized capacities | `ag_CHP_emax`, `ag_ec_cmax`, `ag_ac_cmax`, `ag_hp_hmax`, `ag_b_hmax`, `ag_ele_st_max`, `ag_cool_st_max`, `ag_pv_areamax` |
| Hourly operation | CHP, PV, grid, storage, heating/cooling-device dispatch and inter-building flows |
| Seismic/restoration state | Damage-hour, component-state, and restoration-related quantities |

The released notebook does **not currently export a final CSV/Excel result package automatically**. A validated benchmark output can be added after the authors confirm the final numerical reproduction settings.

## Replication notes

Before running the workflow, confirm that:

1. the selected city workbook remains at `data/<city>/model_data.xlsx`;
2. all seven worksheet names remain unchanged: `dist`, `qty_day`, `e_dem`, `c_dem`, `h_dem`, `price`, and `SRI`;
3. demand and SRI profiles retain the `h1`–`h168` column structure;
4. the building labels remain `b1`–`b6` and scenario labels remain `sum`, `win`, `mid`, `M6`, `M7`, `M8`;
5. `code/config/seismic_probabilities.csv` remains synchronized with the selected city workbook;
6. a valid Gurobi installation and license are available;
7. a small Monte Carlo count is used first when checking installation and path configuration;
8. a fixed random seed and author-retained reference result should be used for the final numerical benchmark before archival release.

The workbook values and scientific model formulation should not be changed solely for repository formatting. Any scientific change should be validated against the manuscript and Supplementary Information before release.

## Status

- The full-cycle Pyomo/Gurobi notebook is included.
- Model workbooks for Beijing, Fuzhou, Harbin, Pu'er, Wuhan, and Xi'an are included.
- City-specific M6/M7/M8 occurrence probabilities are included.
- The current Supplementary Information documents the DES cost objective, base model constraints, and location-specific seismic probability method.
- A standardized exported benchmark-result package has not yet been included.
- Final unit metadata and selected manuscript/code consistency items should be confirmed by the model authors before the repository is frozen for archival release.
