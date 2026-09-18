# Data Entry Automation

A Python CLI tool for validating, cleaning, and exporting structured data from CSV and Excel files.

## What it does

Data Entry Automation turns messy contact data into a consistent, validated dataset. It can:

- Read CSV and XLSX files
- Normalize names, emails, phone numbers, and whitespace
- Validate required fields and email formats
- Separate invalid rows into an error report
- Export cleaned data to CSV or XLSX
- Run from a simple command-line interface

## Input format

The input file must contain these columns:

- `name`
- `email`
- `phone`

The optional `company` column is preserved when present.

Headers are matched case-insensitively and spaces are converted to underscores.

## Installation

Requires Python 3.10 or newer.

```bash
python -m pip install .
```

For development and tests:

```bash
python -m pip install -e ".[test]"
pytest -q
```

## Usage

Process a CSV file and create a cleaned CSV:

```bash
data-entry sample_data/contacts.csv
```

This creates `cleaned_contacts.csv` and `cleaned_contacts_errors.csv`.

Choose an output path:

```bash
data-entry contacts.xlsx --output output/contacts.xlsx --format xlsx
```

The command reports the total number of rows, valid records, validation errors, and generated files.

## Example

The sample input contains both valid and invalid records. Running:

```bash
data-entry sample_data/contacts.csv
```

produces a cleaned dataset containing only valid records. Invalid rows are written to the error report with their row number, field, and validation message.

## Project structure

```text
data-entry-automation/
├── .github/workflows/ci.yml
├── sample_data/contacts.csv
├── src/data_entry_automation/
│   ├── cli.py
│   ├── processor.py
│   └── validators.py
├── tests/
│   ├── test_cli.py
│   ├── test_processor.py
│   └── test_validators.py
└── pyproject.toml
```

## License

MIT
