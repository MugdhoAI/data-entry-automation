"""Validation and normalization helpers."""

from __future__ import annotations

import re
from dataclasses import dataclass


_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(frozen=True)
class ValidationError:
    row: int
    field: str
    message: str


def clean_value(value: object) -> str:
    """Convert a cell to a trimmed string and collapse repeated whitespace."""
    return " ".join(str(value or "").strip().split())


def normalize_email(value: object) -> str:
    """Normalize an email address for consistent storage."""
    return clean_value(value).lower()


def normalize_phone(value: object) -> str:
    """Keep digits and a leading plus sign in phone numbers."""
    raw = clean_value(value)
    if raw.startswith("+"):
        return "+" + re.sub(r"\D", "", raw)
    return re.sub(r"\D", "", raw)


def validate_record(record: dict[str, str], row_number: int) -> list[ValidationError]:
    """Validate a normalized contact record."""
    errors: list[ValidationError] = []

    if not record.get("name"):
        errors.append(ValidationError(row_number, "name", "Name is required."))

    email = record.get("email", "")
    if not email:
        errors.append(ValidationError(row_number, "email", "Email is required."))
    elif not _EMAIL_RE.fullmatch(email):
        errors.append(ValidationError(row_number, "email", "Email format is invalid."))

    if not record.get("phone"):
        errors.append(ValidationError(row_number, "phone", "Phone is required."))

    return errors
