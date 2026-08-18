# Code

`full_cycle_model.ipynb` is the model entry point for the six-city seismic-resilience analysis.

## Notebook map

| Section | Main content |
|---|---|
| **1. Configuration** | imports, city selection, Monte Carlo count, optional random seed, repository path discovery |
| **2. Model index sets** | buildings, hours, scenarios, Monte Carlo realizations, technologies, tariff categories |
| **3. Input data** | reads `dist`, `qty_day`, `e_dem`, `c_dem`, `h_dem`, `price`, `SRI` |
| **4. Fixed techno-economic parameters** | capacity bounds, efficiencies, costs, pipe losses, roof areas, scenario and fragility probabilities |
| **5. Seismic scenarios** | random earthquake onset and stochastic component damage states |
| **6. Optimization model** | energy balances, capacities, devices, storage, grid, networks, unmet demand, restoration, and cost equations |
| **7. Objective function** | minimizes total annualized cost |
| **8. Solve and collect results** | Gurobi solve loop and `m.ag_*` result collection |

## User configuration

For normal use, edit only:

```python
CITY = "harbin"
N_MONTE_CARLO = 1000
RANDOM_SEED = None
```

Accepted city IDs are `beijing`, `fuzhou`, `harbin`, `puer`, `wuhan`, and `xian`.

For a quick functionality check, temporarily set `N_MONTE_CARLO` to `1` or `5`. Use the study-scale value only when a full run is intended.

City metadata are loaded from:

```text
../config/seismic_probabilities.csv
```

The selected Excel workbook is resolved automatically.

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

See [`../docs/DATA_DICTIONARY.md`](../docs/DATA_DICTIONARY.md) for definitions and unit notes.

## Main sets

```text
m.i, m.j : b1 ... b6
m.h      : h1 ... h168
m.s      : sum, win, mid, M6, M7, M8
m.sr     : sr1 ... srN
m.t      : chp, boiler, ec, ac, hp, cool_st, heat_st, ele_st, grid, pv
m.p      : grid_buy1, grid_buy2, grid_sell, NG
```

## Main outputs

The solve loop stores each Monte Carlo realization in `m.ag_*` containers. Important groups include:

- objective and cost terms: `ag_results`, `ag_Disaster_cost`, `ag_device_cost`, `ag_pipe_cost`, `ag_maint_cost`, `ag_fuel_cost`, `ag_grid_im_cost`, `ag_grid_ex_cost`, `ag_restored_cost`;
- resilience metrics: `ag_EENS`, `ag_EIU`;
- optimized capacities: `ag_CHP_emax`, `ag_ec_cmax`, `ag_ac_cmax`, `ag_hp_hmax`, `ag_b_hmax`, `ag_ele_st_max`, `ag_cool_st_max`, `ag_pv_areamax`;
- hourly dispatch/flow: `ag_chp_e`, `ag_pv_e`, `ag_ec_*`, `ag_hp_*`, `ag_grid_*`, `ag_tr_h`, `ag_tr_c`, and storage charge/discharge variables;
- damage-state and restoration-related values.

The notebook does not yet export a final result package to disk. See [`../results/README.md`](../results/README.md) and [`../docs/REPRODUCTION.md`](../docs/REPRODUCTION.md).
