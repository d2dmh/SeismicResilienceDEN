# Code guide

`full_cycle_model.ipynb` is the single public model entry point.

It has been organized for repository use without keeping a second archive copy of the original working notebook. The public notebook therefore contains the research implementation that users should read and run.

## Notebook sections

| Section | Main content |
|---|---|
| **1. Configuration** | imports, city selection, Monte Carlo count, optional random seed, repository path discovery |
| **2. Model index sets** | buildings, hours, scenarios, Monte Carlo realizations, technologies and tariff categories |
| **3. Input data** | reads `dist`, `qty_day`, `e_dem`, `c_dem`, `h_dem`, `price`, `SRI` |
| **4. Fixed techno-economic parameters** | capacity bounds, efficiencies, costs, pipe losses, roof areas, scenario probabilities and fragility probabilities |
| **5. Seismic scenarios** | random earthquake onset and stochastic component damage states |
| **6. Optimization model** | energy balances, capacities, devices, storage, grid, networks, unmet demand, restoration and cost equations |
| **7. Objective function** | minimize total annualized cost |
| **8. Solve and collect results** | Gurobi solve loop and `m.ag_*` result collection |

## User-facing configuration

Change only this block for normal use:

```python
CITY = "harbin"
N_MONTE_CARLO = 1000
RANDOM_SEED = None
```

City metadata are loaded from:

```text
../config/seismic_probabilities.csv
```

The selected Excel path is then resolved automatically.

## Input-to-model mapping

```text
dist     -> m.dist[i, j]
qty_day  -> m.qty_day[s, i]
e_dem    -> m.e_demand[i, s, h]
c_dem    -> m.c_demand[i, s, h]
h_dem    -> m.h_demand[i, s, h]
price    -> m.price[p, h]
SRI      -> m.SRI[s, h]
```

See `../docs/DATA_DICTIONARY.md` for full definitions and unit notes.

## Main sets

```text
m.i, m.j : b1 ... b6
m.h      : h1 ... h168
m.s      : sum, win, mid, M6, M7, M8
m.sr     : sr1 ... srN (N=1000 by default)
m.t      : chp, boiler, ec, ac, hp, cool_st, heat_st, ele_st, grid, pv
m.p      : grid_buy1, grid_buy2, grid_sell, NG
```

## Main outputs retained in memory

The solve loop collects each Monte Carlo realization into `m.ag_*` containers. Important groups include:

- objective and cost terms: `ag_results`, `ag_Disaster_cost`, `ag_device_cost`, `ag_pipe_cost`, `ag_maint_cost`, `ag_fuel_cost`, `ag_grid_im_cost`, `ag_grid_ex_cost`, `ag_restored_cost`;
- resilience metrics: `ag_EENS`, `ag_EIU`;
- optimized capacities: `ag_CHP_emax`, `ag_ec_cmax`, `ag_ac_cmax`, `ag_hp_hmax`, `ag_b_hmax`, `ag_ele_st_max`, `ag_cool_st_max`, `ag_pv_areamax`;
- hourly dispatch/flow: `ag_chp_e`, `ag_pv_e`, `ag_ec_*`, `ag_hp_*`, `ag_grid_*`, `ag_tr_h`, `ag_tr_c`, storage charge/discharge variables;
- restoration and damage-state values.

The notebook currently does not export a final results CSV/Excel file.

## What was reorganized

Repository-facing changes include:

1. explicit imports;
2. one city/Monte-Carlo configuration block;
3. repository-relative data paths;
4. city probability lookup from a readable CSV;
5. normalized input filenames;
6. explanatory notebook sections;
7. removal of stored solver output/execution counters;
8. documentation of inputs, variables, outputs and known manuscript/code synchronization points.

Scientific constraints and embedded parameter values are retained from the supplied model unless explicitly noted in `../docs/MODEL_DESCRIPTION.md`.
