# Reproduction guide

## 1. Environment

Recommended baseline:

- Python 3.10 or later;
- NumPy;
- pandas;
- openpyxl;
- Pyomo;
- Gurobi / gurobipy;
- JupyterLab.

From the repository root:

```bash
python -m venv .venv
pip install -r requirements.txt
```

A valid Gurobi license is required for optimization runs.

## 2. Structural validation without Gurobi

Before running the optimization model, verify the package structure:

```bash
python -m unittest discover -s tests -v
```

This checks the six city files, workbook sheet names, seismic probability configuration, notebook syntax, and documentation links. The same check runs automatically in GitHub Actions.

## 3. Select a city

Open `code/full_cycle_model.ipynb` and edit the user-configuration block:

```python
CITY = "harbin"
N_MONTE_CARLO = 1000
RANDOM_SEED = None
```

Accepted city IDs:

```text
beijing
fuzhou
harbin
puer
wuhan
xian
```

The notebook reads both the city workbook path and M6/M7/M8 probabilities from `config/seismic_probabilities.csv`.

## 4. Choose the run scale

### Smoke test

Use a small number of Monte Carlo realizations to confirm that the local Python/Gurobi environment can build and solve the model:

```python
N_MONTE_CARLO = 1  # or 5
RANDOM_SEED = 2026
```

A smoke test is for software validation only and should **not** be interpreted as a manuscript-scale scientific result.

### Study-scale run

The current study configuration uses:

```python
N_MONTE_CARLO = 1000
RANDOM_SEED = None
```

Because each realization invokes a large optimization model, a full run can be computationally expensive.

## 5. Solver settings

The notebook retains:

```text
Solver: Gurobi
MIPGap: 0.001
TimeLimit: 2400 seconds per solve
```

## 6. Run the notebook

Start Jupyter from the repository root:

```bash
jupyter lab
```

Then open and run:

```text
code/full_cycle_model.ipynb
```

The notebook also searches parent directories for `config/seismic_probabilities.csv`, so repository paths remain resolvable when the working directory is `code/`.

## 7. Results

After each successful solve, model outputs are copied into mutable Pyomo parameters with the prefix `ag_`, including:

```text
m.ag_results
m.ag_Disaster_cost
m.ag_device_cost
m.ag_pipe_cost
m.ag_maint_cost
m.ag_fuel_cost
m.ag_grid_im_cost
m.ag_grid_ex_cost
m.ag_restored_cost
m.ag_EENS
m.ag_EIU
m.ag_CHP_emax
m.ag_ec_cmax
m.ag_ac_cmax
m.ag_hp_hmax
m.ag_b_hmax
m.ag_ele_st_max
m.ag_cool_st_max
m.ag_pv_areamax
m.ag_chp_e
m.ag_pv_e
...
```

The current notebook does not automatically export these objects. The `results/` directory is reserved for author-validated benchmark outputs and future export routines.

## 8. Publication-level validation

Before freezing a journal/Zenodo release, perform at least one controlled reference benchmark:

1. select one city and a fixed random seed;
2. record the exact Python, NumPy, pandas, Pyomo, and Gurobi versions;
3. run the public notebook;
4. export total cost, cost components, EENS/EIU, and key capacities;
5. compare them with an author-retained reference result;
6. store the validated summary under `results/`;
7. tag the verified repository version (for example `v1.0.0`).

This separates repository organization from scientific numerical validation and provides a reproducible reference point for future users.
