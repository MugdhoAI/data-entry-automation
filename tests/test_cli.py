from pathlib import Path

from data_entry_automation.cli import main


def test_cli_processes_csv(tmp_path: Path, monkeypatch, capsys) -> None:
    source = tmp_path / "contacts.csv"
    source.write_text(
        "name,email,phone\nAlice, Alice@Example.COM ,01712-345678\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "sys.argv",
        ["data-entry", str(source), "--output", str(tmp_path / "cleaned.csv")],
    )

    assert main() == 0
    assert (tmp_path / "cleaned.csv").exists()
    assert "Valid: 1" in capsys.readouterr().out
