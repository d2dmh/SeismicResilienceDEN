# Model description

## 1. Purpose

The model represents a distributed energy network (DEN) exposed to stochastic seismic hazards. Its organizing concept is the **Prevention–Adaptation–Restoration (PAR)** full cycle:

1. **Pre-hazard prevention:** select equipment and network capacities;
2. **In-hazard adaptation:** redispatch available electricity/heating/cooling resources after component failures;
3. **Post-hazard restoration:** allow damaged components/network elements to be restored subject to the implementation's repair logic and cost terms.

The optimization is implemented in Pyomo and solved with Gurobi.

## 2. Model dimensions

- buildings: 6 (`b1`–`b6`);
- hourly steps: 168 (`h1`–`h168`);
- representative climate scenarios: `sum`, `win`, `mid`;
- seismic scenarios: `M6`, `M7`, `M8`;
- Monte Carlo realizations: 1000 by default;
- energy vectors: electricity, heating, cooling.

## 3. Objective function

The updated Supplementary Information defines the annualized total cost (ATC) as the sum of:

- capital expenditure (CAPEX);
- fuel cost (FC);
- maintenance cost (MC);
- grid cost (GC);
- unmet demand cost (UDC);
- restoration cost (RC).

The notebook implementation uses `m.obj_TAC` and enforces:

```text
obj_TAC = annualized device cost
        + annualized pipe cost
        + fuel cost
        + grid import cost
        - grid export revenue
        + maintenance cost
        + Disaster_cost
        + restored_cost
```

The final Pyomo objective minimizes `m.obj_TAC`.

### Supplementary mapping

| Supplementary section/equations | Repository implementation |
|---|---|
| Eq. s1–s7: cost objective and cost components | cost variables/constraints in the later model cells; `TAC_limit` and `m.obj` |
| Eq. s8–s10: electricity/heating/cooling balances | `ele_balance*`, `heat_balance*`, `cool_balance*` |
| Eq. s11–s23: capacity, conversion, PV, CHP, storage, grid and network constraints | technology/network cells in `code/full_cycle_model.ipynb` |
| Eq. s24–s27: location-specific seismic probability model | method basis for `config/seismic_probabilities.csv`; numeric city probabilities are supplied inputs |

## 4. Energy-system components

### CHP

- optimized electrical capacity: `CHP_emax`;
- electrical production: `CHP_e`;
- heat-to-power relation controlled by `pH_to_P`;
- minimum part-load and startup/ramping constraints are implemented;
- seismic damage probability and restoration-cost variables are included.

### Boiler

- optimized heating capacity: `b_hmax`;
- heating output: `b_heat`;
- fuel use contributes to natural-gas cost;
- damage and restoration logic included.

### Electric chiller (`ec`)

- optimized cooling capacity: `ec_cmax`;
- electric input: `ec_ele`;
- cooling output: `ec_cool`;
- coefficient of performance is stored in `pEff['ec']`;
- damage and restoration logic included.

### Absorption chiller (`ac`)

- optimized cooling capacity: `ac_cmax`;
- heat input: `ac_heat`;
- cooling output: `ac_cool`;
- damage and restoration logic included.

### Heat pump (`hp`)

- optimized heating capacity: `hp_hmax`;
- electrical input: `hp_ele`;
- heating output: `hp_heat`;
- damage and restoration logic included.

### Electrical storage

- optimized capacity: `ele_st_max`;
- charge/discharge: `ele_cha`, `ele_dis`;
- state variable: `ele_in_st`;
- damage and restoration logic included.

### Cooling storage

- optimized capacity: `cool_st_max`;
- charge/discharge: `cool_cha`, `cool_dis`;
- state variable: `cool_in_st`;
- mutually exclusive charge/discharge constraints included;
- damage and restoration logic included.

### PV

- decision variable `pv_areamax` represents installed PV area;
- output is bounded by `pv_areamax × pEff['pv'] × SRI/1000`;
- `SRI` is in W/m²;
- damage and restoration logic included.

### Utility grid

- import: `grid_im`;
- export: `grid_ex`;
- import/export limits and export restriction are implemented;
- `grid_buy1` is used for `b1`–`b5`, `grid_buy2` for `b6`;
- damage and restoration logic included.

### Heating/cooling networks

- heating transfer: `tr_h` with pipe binary `yPipe_h`;
- cooling transfer: `tr_c` with pipe binary `yPipe_c`;
- distance matrix `dist` contributes to pipe investment;
- pipe damage and restoration variables are included.

## 5. Seismic scenario generation

The notebook embeds fixed technology-specific failure probabilities for each of `M6`, `M7`, and `M8`. For each Monte Carlo realization:

1. earthquake onset hour is sampled uniformly from hours 1–24;
2. each technology/building/scenario draws a random number;
3. the draw is compared against the technology-specific failure probability;
4. a damage hour is assigned when failure occurs; otherwise a sentinel value of 169 is used;
5. the optimization is solved under the resulting component availability states.

The updated Supplementary Information describes the upstream **CPSHA** probability model as follows:

- magnitude distribution follows a truncated Gutenberg–Richter relation;
- magnitude is discretized into intervals;
- annual event count follows a Poisson model;
- annual probability for a magnitude interval is then derived;
- ground-motion intensity is represented by PGA as a function of magnitude and epicentral distance.

The six city-specific M6/M7/M8 values used by the code are stored in `config/seismic_probabilities.csv`.

## 6. Unmet demand and resilience metrics

The model defines unmet electricity, heating and cooling through `ele_loss`, `heat_loss`, and `cool_loss`. These are combined in `load_loss`, and the model computes:

- `Disaster_cost`: monetary penalty based on lost load;
- `EENS`: expected energy not supplied quantity used in the notebook;
- `EIU`: `EENS` divided by a fixed denominator (`3372805`) in the current implementation.

The current repository documents these objects as implemented. It does not reinterpret the fixed EIU denominator because its provenance is not explicitly explained in the current manuscript/data package.

## 7. Restoration-cost parameters

The current notebook uses restoration-cost coefficients consistent with the values presented in the manuscript table for several technologies, including:

- CHP: 80,000;
- heat pump: 50,000;
- absorption chiller: 50,000;
- boiler: 20,000;
- battery/electrical storage: 30,000;
- cooling storage: 30,000;
- grid: 10,000;
- PV: 20,000;
- pipe: 20,000.

The repository retains the code values as the computational source.

## 8. Documentation and validation boundary

The notebook is the executable reference for the current repository release. The manuscript and Supplementary Information describe the corresponding scientific framework, while some implementation-level details (for example exact input units, selected fixed parameters, and complete seismic restoration constraints) should be synchronized by the authors before the final archival release.

No model equation or parameter is altered in this repository solely to resolve a documentation difference. Scientific revisions should be author-approved, numerically benchmarked, and released as a new version.

## 9. Numerical-output boundary

The notebook collects results into mutable Pyomo parameters (`m.ag_*`) but does not export a final results table. This release therefore provides the model implementation and input dataset, while a publication-level numerical benchmark should be added only after author validation.
