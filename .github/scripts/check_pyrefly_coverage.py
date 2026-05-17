from argparse import ArgumentParser
from difflib import unified_diff
from pathlib import Path
import pprint
import json
import sys

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--baseline_report_path",
        type=str,
        required=False,
        default=".pyrefly-baseline-report.json",
    )
    parser.add_argument(
        "--current_report_path",
        type=str,
        required=False,
        default="pyrefly-current-report.json",
    )
    args = parser.parse_args()
    baseline = json.loads(Path(args.baseline_report_path).read_text())
    current = json.loads(Path(args.current_report_path).read_text())

    baseline_reports = {}
    current_reports = {}

    for report in baseline["module_reports"]:
        baseline_reports[report["name"]] = report

    for report in current["module_reports"]:
        current_reports[report["name"]] = report

    failures = []

    for module_name, current_module_report in current_reports.items():
        baseline_module_report = baseline_reports.get(module_name)

        # File does not exist in baseline yet
        if baseline_module_report is None:
            completeness = current_module_report["coverage"]

            if completeness < 100:
                failures.append(
                    f"New file {module_name} is only " f"{completeness:.1f}% annotated"
                )
            continue

        old_n_untpyed = baseline_module_report["n_untyped"]
        new_n_untpyed = current_module_report["n_untyped"]

        if new_n_untpyed > old_n_untpyed:
            dict1_lines = pprint.pformat(
                baseline_module_report, sort_dicts=True
            ).splitlines()
            dict2_lines = pprint.pformat(
                current_module_report, sort_dicts=True
            ).splitlines()

            diff = unified_diff(
                dict1_lines, dict2_lines, fromfile="dict1", tofile="dict2", lineterm=""
            )

            failures.append(
                f"{module_name}: Untyped count increased "
                f"from {old_n_untpyed} to {new_n_untpyed}\n"
                f"\n{'\n'.join(diff)}"
            )

    if failures:
        print("Pyrefly coverage regression detected:")

        for failure in failures:
            print(f"- {failure}\n\n")

        sys.exit(1)

    print("No pyrefly coverage regressions detected.")
