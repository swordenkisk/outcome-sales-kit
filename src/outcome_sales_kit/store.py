from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

from outcome_sales_kit.models import Prospect


class ProspectStore:
    """Simple JSON-backed local prospect store."""

    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir
        self.file_path = data_dir / "prospects.json"

    def initialize(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._write([])

    def all(self) -> list[Prospect]:
        if not self.file_path.exists():
            return []

        try:
            raw_data = json.loads(self.file_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Cannot parse data file: {self.file_path}") from exc

        if not isinstance(raw_data, list):
            raise ValueError("The prospect data file must contain a JSON list.")

        try:
            return [Prospect.from_dict(item) for item in raw_data]
        except (TypeError, KeyError) as exc:
            raise ValueError("The prospect data file has an invalid record.") from exc

    def add(self, prospect: Prospect) -> None:
        prospects = self.all()
        prospects.append(prospect)
        self._write(prospects)

    def get(self, prospect_id: str) -> Prospect:
        for prospect in self.all():
            if prospect.prospect_id == prospect_id:
                return prospect
        raise KeyError(f"No prospect found with ID {prospect_id!r}.")

    def update_stage(self, prospect_id: str, stage: str) -> Prospect:
        prospects = self.all()
        for prospect in prospects:
            if prospect.prospect_id == prospect_id:
                prospect.stage = stage
                self._write(prospects)
                return prospect
        raise KeyError(f"No prospect found with ID {prospect_id!r}.")

    def _write(self, prospects: list[Prospect]) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(
            [prospect.to_dict() for prospect in prospects],
            indent=2,
            ensure_ascii=False,
        )

        file_descriptor, temp_name = tempfile.mkstemp(
            prefix="prospects-",
            suffix=".tmp",
            dir=self.data_dir,
            text=True,
        )
        try:
            with os.fdopen(file_descriptor, "w", encoding="utf-8") as temp_file:
                temp_file.write(payload)
                temp_file.write("\n")
            Path(temp_name).replace(self.file_path)
        except Exception:
            Path(temp_name).unlink(missing_ok=True)
            raise
