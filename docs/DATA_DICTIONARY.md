# Data dictionary

This document maps repository data fields to the Pyomo objects used in `code/full_cycle_model.ipynb`. When a unit or interpretation is **not explicitly defined** in the supplied workbook/manuscript/Supplementary Information, that uncertainty is stated rather than filled in from assumption.

## Core indices

| Repository label | Pyomo set/index | Meaning |
|---|---|---|
| `b1`–`b6` | `m.i`, `m.j` | six representative buildings |
| `h1`–`h168` | `m.h` | 168 hourly time steps (7×24 h) |
| `sum` | `m.s` | summer representative condition |
| `win` | `m.s` | winter representative condition |
| `mid` | `m.s` | transition-season representative condition |
| `M6`, `M7`, `M8` | `m.s` | seismic magnitude scenarios |
| `sr1`–`srN` | `m.sr` | Monte Carlo realization index; `N=1000` by default |

## Workbook-level dictionary

### `dist`

| Item | Definition |
|---|---|
| file location | `data/<city>/model_data.xlsx` |
| worksheet | `dist` |
| row labels | `b1`–`b6` |
| column labels | `b1`–`b6` |
| Pyomo mapping | `m.dist[i, j]` |
| model role | heating/cooling pipe investment and network calculations |
| unit | **not explicitly labelled**; pipe-loss parameters are defined per 1000 m, so metres are the working interpretation |
| special values | `100000` occurs for multiple pairs; exact meaning is not explicitly documented |

### `qty_day`

| Item | Definition |
|---|---|
| worksheet | `qty_day` |
| row labels | `b1`–`b6` |
| columns | `sum`, `win`, `mid`, `M6`, `M7`, `M8` |
| Pyomo mapping | `m.qty_day[s, i]` |
| model role | multiplier in annualized fuel, grid, maintenance, unmet-demand and other cost terms |
| unit | dimensionless multiplicity; exact nomenclature is not explicitly defined |
| implementation note | each underlying profile is 168 h, so the values operate as representative-period weights in the code |

### `e_dem`

| Item | Definition |
|---|---|
| worksheet | `e_dem` |
| first row index | building `b1`–`b6` |
| second row index | `sum`, `win`, `mid`, `M6`, `M7`, `M8` |
| columns | `h1`–`h168` |
| Pyomo mapping | `m.e_demand[i, s, h]` |
| meaning | electricity demand |
| unit | **not explicitly labelled in the workbook** |

### `c_dem`

| Item | Definition |
|---|---|
| worksheet | `c_dem` |
| indexing | building × scenario × `h1`–`h168` |
| Pyomo mapping | `m.c_demand[i, s, h]` |
| meaning | cooling demand |
| unit | **not explicitly labelled in the workbook** |

### `h_dem`

| Item | Definition |
|---|---|
| worksheet | `h_dem` |
| indexing | building × scenario × `h1`–`h168` |
| Pyomo mapping | `m.h_demand[i, s, h]` |
| meaning | heating demand |
| unit | **not explicitly labelled in the workbook** |

### `price`

| Row | Pyomo mapping | Applied to | Unit status |
|---|---|---|---|
| `grid_buy1` | `m.price['grid_buy1', h]` | purchased grid electricity for `b1`–`b5` | not explicitly labelled |
| `grid_buy2` | `m.price['grid_buy2', h]` | purchased grid electricity for `b6` | not explicitly labelled |
| `grid_sell` | `m.price['grid_sell', h]` | exported electricity/feed-in revenue | not explicitly labelled |
| `NG` | `m.price['NG', h]` | CHP and boiler fuel cost | not explicitly labelled |

All four rows contain `h1`–`h168` values.

### `SRI`

| Item | Definition |
|---|---|
| worksheet | `SRI` |
| rows | `sum`, `win`, `mid`, `M6`, `M7`, `M8` |
| columns | `h1`–`h168` |
| Pyomo mapping | `m.SRI[s, h]` |
| meaning | solar radiation index |
| unit | **W/m²** |
| PV relation | `pv_e <= pv_areamax × pEff['pv'] × SRI/1000` |

## Seismic probability configuration

File: `config/seismic_probabilities.csv`

| Column | Meaning |
|---|---|
| `city_id` | command/configuration identifier used in the notebook |
| `city` | English city name |
| `city_zh` | Chinese city name |
| `climate_group` | `north` or `south` grouping used in the study comparison |
| `seismic_risk_group` | `high`, `medium`, or `low` study grouping |
| `data_file` | repository-relative Excel path |
| `M6` | supplied annual occurrence probability for the M6 scenario |
| `M7` | supplied annual occurrence probability for the M7 scenario |
| `M8` | supplied annual occurrence probability for the M8 scenario |
| `normal_probability` | rounded `1 - (M6 + M7 + M8)` value used by the notebook for the normal/summer probability term |

The updated Supplementary Information describes a CPSHA workflow based on the GB18306-2015 China Seismic Parameter Zoning Map, truncated Gutenberg–Richter magnitude distribution, a Poisson occurrence model, and PGA as a function of magnitude and epicentral distance. The complete region-specific coefficient set required to reconstruct every numeric probability in the CSV is not included in the current release.

## Technology abbreviations used in the notebook

| Code | Meaning |
|---|---|
| `chp` | combined heat and power |
| `boiler` | boiler |
| `ec` | electric chiller |
| `ac` | absorption chiller |
| `hp` | heat pump |
| `cool_st` | cooling storage |
| `heat_st` | heat storage index retained in technology sets; not fully active in all constraint blocks |
| `ele_st` | electrical/battery storage |
| `grid` | utility grid |
| `pv` | photovoltaic system |

## Main in-memory result names

The current notebook does not write final result files automatically. Key values collected during the Monte Carlo loop include:

| Result object | Meaning in code |
|---|---|
| `m.ag_results` | total annualized objective value per Monte Carlo realization |
| `m.ag_Disaster_cost` | unmet-demand/disaster cost |
| `m.ag_device_cost` | annualized device capital cost |
| `m.ag_pipe_cost` | annualized pipe capital cost |
| `m.ag_maint_cost` | maintenance cost |
| `m.ag_fuel_cost` | fuel cost |
| `m.ag_grid_im_cost` | grid import cost |
| `m.ag_grid_ex_cost` | grid export revenue term |
| `m.ag_restored_cost` | restoration cost |
| `m.ag_EENS` | expected energy not supplied metric used by the model |
| `m.ag_EIU` | EENS normalized by the fixed denominator used in the notebook |
| `m.ag_CHP_emax`, etc. | optimized technology capacities |
| `m.ag_chp_e`, `m.ag_pv_e`, etc. | hourly dispatch values |
