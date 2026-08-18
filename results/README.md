# Results

This directory is reserved for **versioned, author-validated model outputs**.

The current notebook stores Monte Carlo results in memory using mutable Pyomo parameters named `m.ag_*`; it does not automatically export a final CSV/Excel package. Generated files should therefore not be treated as manuscript reference results unless they have been explicitly validated and versioned by the study authors.

Recommended future contents include:

- `benchmark_summary.csv` — one fixed-seed reference run with total cost, cost components, EENS/EIU, and key capacities;
- `environment.txt` — Python/Pyomo/Gurobi versions used for the reference run;
- optional figure-source tables used for manuscript plotting.

See [`../docs/REPRODUCTION.md`](../docs/REPRODUCTION.md) for the recommended validation workflow.
