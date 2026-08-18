# Input data

The `data/` directory contains the six city-specific model workbooks used by the public notebook. Every workbook has been renamed to the stable filename `model_data.xlsx`; the worksheet names and numerical data are retained in the model-compatible structure.

## Files

| Folder | City | Workbook | Climate group | Seismic-risk group |
|---|---|---|---|---|
| `beijing/` | Beijing / 北京 | `model_data.xlsx` | North | Medium |
| `fuzhou/` | Fuzhou / 福州 | `model_data.xlsx` | South | Medium |
| `harbin/` | Harbin / 哈尔滨 | `model_data.xlsx` | North | Low |
| `puer/` | Pu'er / 普洱 | `model_data.xlsx` | South | Low |
| `wuhan/` | Wuhan / 武汉 | `model_data.xlsx` | South | High |
| `xian/` | Xi'an / 西安 | `model_data.xlsx` | North | High |

`DATA_MANIFEST.csv` provides a compact machine-readable inventory of the six workbooks, including the original source filename, normalized path, file size, SHA256 checksum, worksheet list, profile length, and representative-period multiplicities.

## Common workbook schema

All six files contain exactly seven model sheets:

### 1. `dist`

**Purpose:** spatial/network input used in heating and cooling pipe capital-cost and network calculations.

- rows: `b1`–`b6`;
- columns: `b1`–`b6`;
- data block: 6×6 pairwise distance matrix;
- model mapping: `m.dist[i, j]`.

The workbook itself does **not explicitly label the unit**. The model defines heating/cooling pipe loss rates per 1000 m, so metres are the working interpretation, but this should be confirmed by the original data author. Several cells contain `100000`; these act as very large distance/penalty-like values in the supplied model input, but their exact semantic meaning is not explicitly documented and is therefore not reinterpreted here.

### 2. `qty_day`

**Purpose:** multiplicity used to annualize each representative profile in cost calculations.

- rows: `b1`–`b6`;
- columns: `sum`, `win`, `mid`, `M6`, `M7`, `M8`;
- model mapping: `m.qty_day[s, i]`.

Although the variable/sheet name is `qty_day`, the associated demand and price profiles contain **168 hourly values (7×24 h)**. The code multiplies each 168-hour profile by these values when annualizing cost terms. Therefore the values function as representative-period multiplicities in the implementation rather than literal hourly data.

City-level values are identical across `b1`–`b6` within each workbook:

| City | `sum` | `win` | `mid` | `M6` | `M7` | `M8` |
|---|---:|---:|---:|---:|---:|---:|
| Beijing | 11 | 17 | 24 | 11 | 11 | 11 |
| Fuzhou | 17 | 13 | 22 | 17 | 17 | 17 |
| Harbin | 11 | 22 | 19 | 11 | 11 | 11 |
| Pu'er | 19 | 13 | 20 | 19 | 19 | 19 |
| Wuhan | 17 | 17 | 17 | 17 | 17 | 17 |
| Xi'an | 16 | 16 | 20 | 16 | 16 | 16 |

The precise terminology for these multiplicities is not explicitly defined in the supplied spreadsheet, so the repository avoids renaming the original field.

### 3. `e_dem`

**Purpose:** electricity-demand input.

- row index 1: building (`b1`–`b6`);
- row index 2: scenario (`sum`, `win`, `mid`, `M6`, `M7`, `M8`);
- columns: `h1`–`h168`;
- model mapping: `m.e_demand[i, s, h]`.

The workbook does **not explicitly include a demand unit in the header**. The notebook treats each value as an hourly load/power input and uses it directly in the electricity balance.

### 4. `c_dem`

**Purpose:** cooling-demand input.

- same indexing as `e_dem`;
- columns: `h1`–`h168`;
- model mapping: `m.c_demand[i, s, h]`.

The workbook does **not explicitly include a demand unit**.

### 5. `h_dem`

**Purpose:** heating-demand input.

- same indexing as `e_dem`;
- columns: `h1`–`h168`;
- model mapping: `m.h_demand[i, s, h]`.

The workbook does **not explicitly include a demand unit**.

### 6. `price`

**Purpose:** time-varying grid and fuel prices.

Rows are:

| Row label | Model use |
|---|---|
| `grid_buy1` | grid purchase tariff applied to `b1`–`b5` |
| `grid_buy2` | grid purchase tariff applied to `b6` |
| `grid_sell` | electricity export/feed-in tariff |
| `NG` | natural-gas price used for CHP and boiler fuel cost |

Columns are `h1`–`h168`. The file does **not explicitly state the monetary/energy unit**. The notebook uses these values directly as unit energy prices in the annual cost equations.

### 7. `SRI`

**Purpose:** solar radiation input for PV generation.

- rows: `sum`, `win`, `mid`, `M6`, `M7`, `M8`;
- columns: `h1`–`h168`;
- model mapping: `m.SRI[s, h]`;
- unit: **W/m²**, explicitly described in the Supplementary Information.

The notebook uses:

```text
PV output ≤ PV area × PV efficiency × (SRI / 1000)
```

For the seismic scenarios, the supplied `SRI` profiles repeat the corresponding summer profile structure in the current workbooks.

## Scenario labels

| Label | Meaning in the repository |
|---|---|
| `sum` | summer representative condition |
| `win` | winter representative condition |
| `mid` | transition-season representative condition |
| `M6` | magnitude-6 seismic condition used by the model |
| `M7` | magnitude-7 seismic condition used by the model |
| `M8` | magnitude-8 seismic condition used by the model |

The city-level **annual occurrence probabilities** for `M6`, `M7`, and `M8` are stored separately in `../config/seismic_probabilities.csv`; they are not embedded in the Excel files.

## Relation to the Supplementary Data Set

The updated Supplementary Information describes the Supplementary Data Set as containing: (1) hourly load profiles for all case cities, (2) market-oriented feed-in tariff and gas-price data, and (3) seasonal solar radiation index data. These correspond directly to the `e_dem`/`c_dem`/`h_dem`, `price`, and `SRI` sheets in this repository.

For field-by-field mappings to Pyomo objects, see [`../docs/DATA_DICTIONARY.md`](../docs/DATA_DICTIONARY.md).
