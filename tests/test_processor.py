from pathlib import Path

from data_entry_automation.processor import process_file, write_csv


def test_process_file_cleans_and_separates_invalid_rows(tmp_path: Path) -> None:
    source = tmp_path / "contacts.csv"
    source.write_text(
        "name,email,phone,company\n"
        " Alice Rahman , Alice@Example.COM , +880 1712-345678 , Example Ltd\n"
        "Missing Email,,01712345678,Acme\n",
        encoding="utf-8",
    )

    result = process_file(source)

    assert result.total_rows == 2
    assert result.records == [
        {
            "name": "Alice Rahman",
            "email": "alice@example.com",
            "phone": "+8801712345678",
            "company": "Example Ltd",
        }
    ]
    assert result.errors == [
        {"row": 3, "field": "email", "message": "Email is required."}
    ]


def test_write_csv(tmp_path: Path) -> None:
    output = tmp_path / "cleaned.csv"
    write_csv(
        output,
        [
            {
                "name": "Alice",
                "email": "alice@example.com",
                "phone": "01700000000",
                "company": "Example",
            }
        ],
    )

    assert output.read_text(encoding="utf-8") == (
        "name,email,phone,company\n"
        "Alice,alice@example.com,01700000000,Example\n"
    )
