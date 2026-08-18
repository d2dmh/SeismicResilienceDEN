import csv
import json
import unittest
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CITIES = {
    "beijing": ("Beijing", "北京", "north", "medium", 0.015274137, 0.002311834, 0.00034991),
    "fuzhou": ("Fuzhou", "福州", "south", "medium", 0.0065, 0.0008, 0.0004),
    "harbin": ("Harbin", "哈尔滨", "north", "low", 0.0106, 0.0001, 0.0000303),
    "puer": ("Pu'er", "普洱", "south", "low", 0.000222626, 0.0000378073, 0.0000075),
    "wuhan": ("Wuhan", "武汉", "south", "high", 0.04826, 0.006817, 0.00096),
    "xian": ("Xi'an", "西安", "north", "high", 0.06974701, 0.011575122, 0.001920992),
}
EXPECTED_SHEETS = ["dist", "qty_day", "e_dem", "c_dem", "h_dem", "price", "SRI"]


def xlsx_sheet_names(path: Path):
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(path) as zf:
        root = ET.fromstring(zf.read("xl/workbook.xml"))
    return [node.attrib["name"] for node in root.find("m:sheets", ns)]


class RepositoryIntegrityTests(unittest.TestCase):
    def test_repository_contains_only_clean_public_code(self):
        self.assertFalse((ROOT / "original").exists(), "public package must not retain original/ archive")
        self.assertTrue((ROOT / "code" / "full_cycle_model.ipynb").exists())
        self.assertFalse((ROOT / "code" / "full_cycle_seismic_model.ipynb").exists())

    def test_seismic_probability_csv_is_complete(self):
        path = ROOT / "config" / "seismic_probabilities.csv"
        self.assertTrue(path.exists(), "config/seismic_probabilities.csv should exist")
        with path.open(encoding="utf-8-sig", newline="") as f:
            rows = {row["city_id"]: row for row in csv.DictReader(f)}
        self.assertEqual(set(rows), set(EXPECTED_CITIES))
        for city, expected in EXPECTED_CITIES.items():
            display, zh, climate, risk, m6, m7, m8 = expected
            row = rows[city]
            self.assertEqual(row["city"], display)
            self.assertEqual(row["city_zh"], zh)
            self.assertEqual(row["climate_group"], climate)
            self.assertEqual(row["seismic_risk_group"], risk)
            self.assertAlmostEqual(float(row["M6"]), m6)
            self.assertAlmostEqual(float(row["M7"]), m7)
            self.assertAlmostEqual(float(row["M8"]), m8)
            self.assertAlmostEqual(float(row["normal_probability"]), round(1.0 - (m6 + m7 + m8), 4))
            self.assertEqual(row["data_file"], f"data/{city}/model_data.xlsx")

    def test_each_city_workbook_has_expected_structure(self):
        for city in EXPECTED_CITIES:
            path = ROOT / "data" / city / "model_data.xlsx"
            self.assertTrue(path.exists(), f"missing {path.relative_to(ROOT)}")
            self.assertEqual(xlsx_sheet_names(path), EXPECTED_SHEETS)

    def test_clean_notebook_is_configurable_documented_and_syntax_valid(self):
        path = ROOT / "code" / "full_cycle_model.ipynb"
        nb = json.loads(path.read_text(encoding="utf-8"))
        code_cells = [c for c in nb["cells"] if c.get("cell_type") == "code"]
        code = "\n".join("".join(c.get("source", [])) for c in code_cells)
        markdown = "\n".join("".join(c.get("source", [])) for c in nb["cells"] if c.get("cell_type") == "markdown")
        self.assertIn("CITY =", code)
        self.assertIn("N_MONTE_CARLO =", code)
        self.assertIn("seismic_probabilities.csv", code)
        self.assertIn("DATA_FILE", code)
        self.assertNotIn("cities.json", code)
        self.assertNotIn("哈尔滨模型数据.xlsx", code)
        for heading in ["Configuration", "Input data", "Seismic scenarios", "Optimization model", "Solve and collect results"]:
            self.assertIn(heading, markdown)
        for cell in code_cells:
            self.assertEqual(cell.get("outputs", []), [])
            self.assertIsNone(cell.get("execution_count"))
            compile("".join(cell.get("source", [])), "<notebook-cell>", "exec")

    def test_public_documentation_is_complete(self):
        required = [
            "README.md",
            "requirements.txt",
            ".gitignore",
            "CITATION.cff",
            "data/README.md",
            "data/DATA_MANIFEST.csv",
            "code/README.md",
            "docs/DATA_DICTIONARY.md",
            "docs/MODEL_DESCRIPTION.md",
            "docs/REPRODUCTION.md",
        ]
        for rel in required:
            self.assertTrue((ROOT / rel).exists(), f"missing {rel}")
        self.assertFalse((ROOT / "docs" / "KNOWN_ISSUES.md").exists())
        self.assertFalse((ROOT / "docs" / "MODEL_NOTES.md").exists())

    def test_data_documentation_names_every_sheet_and_key_index(self):
        text = ((ROOT / "data" / "README.md").read_text(encoding="utf-8") + "\n" +
                (ROOT / "docs" / "DATA_DICTIONARY.md").read_text(encoding="utf-8"))
        for name in EXPECTED_SHEETS + ["b1", "b6", "h1", "h168", "grid_buy1", "grid_buy2", "grid_sell", "NG", "M6", "M7", "M8"]:
            self.assertIn(name, text)
        self.assertIn("unit", text.lower())
        self.assertIn("not explicitly", text.lower())

    def test_publication_readme_has_clean_first_screen_and_navigation(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Spatiotemporal full-cycle optimal design enhances seismic resilience of distributed energy networks", text)
        self.assertIn("```mermaid", text)
        self.assertIn("Repository guide", text)
        self.assertIn("Quick validation", text)
        self.assertNotIn("original working folders", text)
        self.assertNotIn("supplied research materials", text)

    def test_github_integrity_workflow_is_included(self):
        path = ROOT / ".github" / "workflows" / "repository-integrity.yml"
        self.assertTrue(path.exists())
        text = path.read_text(encoding="utf-8")
        self.assertIn("python -m unittest discover -s tests -v", text)

    def test_results_directory_is_preserved_for_github(self):
        self.assertTrue((ROOT / "results" / "README.md").exists())
        self.assertTrue((ROOT / "results" / ".gitkeep").exists())


if __name__ == "__main__":
    unittest.main()
