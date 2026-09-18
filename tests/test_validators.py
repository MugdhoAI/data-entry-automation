from data_entry_automation.validators import (
    clean_value,
    normalize_email,
    normalize_phone,
    validate_record,
)


def test_clean_value_normalizes_whitespace() -> None:
    assert clean_value("  Alice   Rahman  ") == "Alice Rahman"


def test_normalize_email() -> None:
    assert normalize_email(" Alice@Example.COM ") == "alice@example.com"


def test_normalize_phone() -> None:
    assert normalize_phone("+880 1712-345678") == "+8801712345678"
    assert normalize_phone("01712-345678") == "01712345678"


def test_validate_record_reports_missing_and_invalid_fields() -> None:
    errors = validate_record(
        {"name": "", "email": "bad", "phone": ""},
        row_number=4,
    )

    assert {(error.field, error.message) for error in errors} == {
        ("name", "Name is required."),
        ("email", "Email format is invalid."),
        ("phone", "Phone is required."),
    }
