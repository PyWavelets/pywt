import pytest
import json
from pathlib import Path
from pytest import fixture
from typing import Iterator

def pytest_configure(config):
    config.addinivalue_line("markers",
                            "slow: Tests that are slow.")


@fixture
def baseline_report(tmp_path: Path) -> Iterator[Path]:
    baseline_report_path = tmp_path / "pyrefly-test-baseline-report.json"

    mock_content = {
        "module_reports": [
            {
                "name": "test_file",
                "names": [
                    "test_file.function1",
                    "test_file.function2",
                ],
                "line_count": 100,
                "symbol_reports": [
                    {
                        "kind": "function",
                        "name": "test_file.function1",
                        "n_typable": 5,
                        "n_typed": 0,
                        "n_any": 0,
                        "n_untyped": 5,
                        "location": {"line": 20, "column": 1},
                    },
                    {
                        "kind": "function",
                        "name": "test_file.function2",
                        "n_typable": 5,
                        "n_typed": 5,
                        "n_any": 0,
                        "n_untyped": 0,
                        "location": {"line": 80, "column": 1},
                    },
                ],
                "type_ignores": [],
                "n_typable": 10,
                "n_typed": 5,
                "n_any": 0,
                "n_untyped": 5,
                "coverage": 50.0,  # 5/10
            }
        ],
        "summary": {
            "n_modules": 1,
            "n_typable": 10,
            "n_typed": 5,
            "n_any": 0,
            "n_untyped": 5,
            "coverage": 50.0,  # 5/10
        },
    }

    with open(baseline_report_path, "w") as fp:
        json.dump(mock_content, fp)

    yield baseline_report_path

    # Cleanup report file
    baseline_report_path.unlink()

