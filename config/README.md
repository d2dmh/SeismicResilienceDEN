# Seismic probability configuration

`seismic_probabilities.csv` is the notebook's city-level configuration table.

Each row links one city to:

- its normalized repository workbook path;
- north/south climate grouping used in the study;
- high/medium/low seismic-risk grouping;
- supplied annual occurrence probabilities for `M6`, `M7`, and `M8`;
- `normal_probability`, stored at the precision used by the organized notebook.

The updated Supplementary Information explains the upstream CPSHA method (truncated magnitude-frequency relationship, Poisson annual occurrence model, and PGA calculation), but the current public package does not contain every regional coefficient needed to independently regenerate the six final probability triplets. Therefore the CSV values are treated as supplied inputs.

To run another case, edit `CITY` in `code/full_cycle_model.ipynb`; do not manually rewrite the Excel path or probabilities in the model cells.
