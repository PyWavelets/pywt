import json
from pathlib import Path
import shutil
import subprocess
import sys


def test_no_changes_implies_no_regression(baseline_report: Path, tmp_path: Path):

    current_report = tmp_path / "pyrefly-test-current-report.json"

    shutil.copy(baseline_report, current_report)

    process: subprocess.CompletedProcess = subprocess.run(
        [
            sys.executable,
            ".github/scripts/check_pyrefly_coverage.py",
            "--baseline_report_path",
            baseline_report,
            "--current_report_path",
            current_report,
        ],
        capture_output=True,
        text=True,
    )
    assert process.returncode == 0
    assert process.stdout == "No pyrefly coverage regressions detected.\n"


def test_increasing_type_coverage_implies_no_regression(
    baseline_report: Path, tmp_path: Path
):

    current_report = tmp_path / "pyrefly-test-current-report.json"

    shutil.copy(baseline_report, current_report)

    data = json.loads(current_report.read_text())
    data["module_reports"][0]["symbol_reports"][0]["n_typed"] += 1
    data["module_reports"][0]["symbol_reports"][0]["n_untyped"] -= 1
    data["module_reports"][0]["n_typed"] += 1
    data["module_reports"][0]["n_untyped"] -= 1
    data["module_reports"][0]["coverage"] += 10
    data["summary"]["coverage"] += 10

    current_report.write_text(json.dumps(data))

    process: subprocess.CompletedProcess = subprocess.run(
        [
            sys.executable,
            ".github/scripts/check_pyrefly_coverage.py",
            "--baseline_report_path",
            baseline_report,
            "--current_report_path",
            current_report,
        ],
        capture_output=True,
        text=True,
    )
    assert process.returncode == 0
    assert process.stdout == "No pyrefly coverage regressions detected.\n"


def test_decreasing_type_coverage_implies_regression(
    baseline_report: Path, tmp_path: Path
):

    current_report = tmp_path / "pyrefly-test-current-report.json"

    shutil.copy(baseline_report, current_report)

    data = json.loads(current_report.read_text())
    data["module_reports"][0]["symbol_reports"][1]["n_typed"] -= 1
    data["module_reports"][0]["symbol_reports"][1]["n_untyped"] += 1
    data["module_reports"][0]["n_typed"] -= 1
    data["module_reports"][0]["n_untyped"] += 1
    data["module_reports"][0]["coverage"] -= 10
    data["summary"]["coverage"] -= 10

    current_report.write_text(json.dumps(data))

    process: subprocess.CompletedProcess = subprocess.run(
        [
            sys.executable,
            ".github/scripts/check_pyrefly_coverage.py",
            "--baseline_report_path",
            baseline_report,
            "--current_report_path",
            current_report,
        ],
        capture_output=True,
        text=True,
    )
    assert process.returncode == 1
    assert "Pyrefly coverage regression detected" in process.stdout
    assert "Untyped count increased from 5 to 6" in process.stdout


def test_adding_fully_annotated_file_implies_no_regression(
    baseline_report: Path, tmp_path: Path
):

    current_report = tmp_path / "pyrefly-test-current-report.json"

    shutil.copy(baseline_report, current_report)

    data = json.loads(current_report.read_text())
    data["module_reports"].append(
        {
            "name": "new_test_file",
            "names": [
                "new_test_file.function1",
            ],
            "line_count": 100,
            "symbol_reports": [
                {
                    "kind": "function",
                    "name": "test_file.function1",
                    "n_typable": 5,
                    "n_typed": 5,
                    "n_any": 0,
                    "n_untyped": 0,
                    "location": {"line": 1, "column": 1},
                },
            ],
            "type_ignores": [],
            "n_typable": 5,
            "n_typed": 5,
            "n_any": 0,
            "n_untyped": 0,
            "coverage": 100.0,
        }
    )
    data["summary"]["coverage"] = 75  # 10/15

    current_report.write_text(json.dumps(data))

    process: subprocess.CompletedProcess = subprocess.run(
        [
            sys.executable,
            ".github/scripts/check_pyrefly_coverage.py",
            "--baseline_report_path",
            baseline_report,
            "--current_report_path",
            current_report,
        ],
        capture_output=True,
        text=True,
    )
    assert process.returncode == 0
    assert process.stdout == "No pyrefly coverage regressions detected.\n"


def test_adding_partially_annotated_file_implies_regression(
    baseline_report: Path, tmp_path: Path
):

    current_report = tmp_path / "pyrefly-test-current-report.json"

    shutil.copy(baseline_report, current_report)

    data = json.loads(current_report.read_text())
    data["module_reports"].append(
        {
            "name": "new_test_file",
            "names": [
                "new_test_file.function1",
            ],
            "line_count": 100,
            "symbol_reports": [
                {
                    "kind": "function",
                    "name": "test_file.function1",
                    "n_typable": 5,
                    "n_typed": 4,
                    "n_any": 0,
                    "n_untyped": 1,
                    "location": {"line": 1, "column": 1},
                },
            ],
            "type_ignores": [],
            "n_typable": 5,
            "n_typed": 4,
            "n_any": 0,
            "n_untyped": 1,
            "coverage": 80.0,
        }
    )
    data["summary"]["coverage"] = 60  # 9/15

    current_report.write_text(json.dumps(data))

    process: subprocess.CompletedProcess = subprocess.run(
        [
            sys.executable,
            ".github/scripts/check_pyrefly_coverage.py",
            "--baseline_report_path",
            baseline_report,
            "--current_report_path",
            current_report,
        ],
        capture_output=True,
        text=True,
    )
    assert process.returncode == 1
    assert r"New file new_test_file is only 80.0% annotated" in process.stdout
