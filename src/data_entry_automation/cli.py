"""Command-line interface for data entry automation."""

from __future__ import annotations

import argparse
from pathlib import Path

from .processor import process_file, write_csv, write_errors, write_xlsx


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="data-entry",
        description="Clean, validate, and export CSV or Excel data.",
    )
    parser.add_argument("input", type=Path, help="Input .csv or .xlsx file.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output file. Defaults to cleaned_<input-name>.<format>.",
    )
    parser.add_argument(
        "--format",
        choices=("csv", "xlsx"),
        default="csv",
        help="Output format (default: csv).",
    )
    parser.add_argument(
        "--errors",
        type=Path,
        help="Optional CSV file for validation errors.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if not args.input.exists():
        print(f"Error: input file not found: {args.input}")
        return 2

    output = args.output or args.input.with_name(
        f"cleaned_{args.input.stem}.{args.format}"
    )
    error_file = args.errors or output.with_name(f"{output.stem}_errors.csv")

    try:
        result = process_file(args.input)
        output.parent.mkdir(parents=True, exist_ok=True)
        error_file.parent.mkdir(parents=True, exist_ok=True)

        if args.format == "csv":
            write_csv(output, result.records)
        else:
            write_xlsx(output, result.records)

        write_errors(error_file, result.errors)
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}")
        return 1

    print(f"Processed: {result.total_rows} rows")
    print(f"Valid: {len(result.records)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Output: {output}")
    print(f"Error report: {error_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
