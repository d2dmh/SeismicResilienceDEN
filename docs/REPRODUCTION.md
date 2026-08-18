# Reproduction guide

## 1. Environment

Recommended:

- Python 3.10 or later;
- NumPy;
- pandas;
- openpyxl (used by pandas to read `.xlsx` files);
- Pyomo;
- Gurobi / gurobipy;
- JupyterLab.

Install Python packages from the repository root:

```bash
python -m venv .venv
```

Activate the environment and run:

```bash
pip install -r requirements.txt
```

A valid Gurobi license is required.

## 2. Select a city

Open `code/full_cycle_model.ipynb` and edit only the user-configuration block unless you intentionally want to change model assumptions:

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

The notebook reads the city workbook path and M6/M7/M8 probabilities from:

```text
config/seismic_probabilities.csv
```

## 3. Run from the repository root

Starting Jupyter from the repository root makes path resolution straightforward:

```bash
jupyter lab
```

Then open and run:

```text
code/full_cycle_model.ipynb
```

The notebook also searches parent directories for `config/seismic_probabilities.csv`, so it can still locate the repository root when the working directory is inside `code/`.

## 4. Input validation before a run

For the selected city, confirm:

```text
data/<city>/model_data.xlsx
```

contains these sheets:

```text
dist
qty_day
e_dem
c_dem
h_dem
price
SRI
```

The demand sheets must retain the two-level row index (building + scenario) and `h1`–`h168` columns.

## 5. Monte Carlo behavior

Default:

```python
N_MONTE_CARLO = 1000
RANDOM_SEED = None
```

With `RANDOM_SEED = None`, stochastic event-time and component-failure draws change between runs. If a reproducible debugging run is needed, set a fixed integer, for example:

```python
RANDOM_SEED = 2026
```

A fixed seed is a repository convenience for reproducibility; the supplied manuscript materials do not explicitly report a historical seed used for the published calculations.

## 6. Solver settings

The notebook retains:

```text
Solver: Gurobi
MIPGap: 0.001
TimeLimit: 2400 seconds per solve
```

Because the default Monte Carlo count is 1000, a complete run can be computationally expensive.

## 7. Results produced by the notebook

After each successful solve, the notebook copies results into mutable Pyomo parameters with the prefix `ag_`.

Examples:

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

The current notebook does **not** automatically export these arrays to disk. `results/` is reserved for future result-export scripts/files.

## 8. Repository-level verification

Before uploading or sharing the repository, run:

```bash
python -m unittest discover -s tests -v
```

The tests check:

- the six city files and sheet names;
- seismic-probability configuration values;
- absence of an archive/original-code folder;
- notebook path configuration and syntax compilation;
- notebook outputs/execution counters are cleared;
- required documentation exists.

This is a structural verification only. It does not invoke Gurobi and does not prove numerical agreement with manuscript figures.

## 9. Recommended archival validation

Before a final journal/Zenodo release, the model authors should ideally perform one controlled numerical benchmark:

1. select one city and one fixed random seed;
2. run the current public notebook;
3. compare total cost, cost components, EENS/EIU and key capacities against an author-retained reference run;
4. document solver/Python/Pyomo/Gurobi versions;
5. only then freeze a versioned archival release.

This step is intentionally separated from the repository-cleaning work so that code organization is not confused with scientific revalidation.
