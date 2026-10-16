from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any
from uuid import uuid4

STAGES = ("new", "qualified", "demo", "proposal", "won", "lost")
PRICING_MODELS = ("retainer", "saas")


def parse_amount(value: str) -> str:
    """Validate a non-negative decimal amount and return its normalized form."""
    try:
        amount = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError(f"Invalid amount: {value!r}") from exc

    if not amount.is_finite() or amount < 0:
        raise ValueError("Amounts must be finite and non-negative.")

    return format(amount.quantize(Decimal("0.01")), "f")


@dataclass
class Prospect:
    prospect_id: str
    name: str
    company: str
    niche: str
    main_pain: str
    desired_outcome: str
    pricing_model: str
    setup_fee: str
    monthly_fee: str
    currency: str
    stage: str
    created_at: str

    @classmethod
    def create(
        cls,
        *,
        name: str,
        company: str,
        niche: str,
        main_pain: str,
        desired_outcome: str,
        pricing_model: str,
        setup_fee: str,
        monthly_fee: str,
        currency: str,
    ) -> "Prospect":
        cleaned = {
            "name": name.strip(),
            "company": company.strip(),
            "niche": niche.strip(),
        }
        for field, value in cleaned.items():
            if not value:
                raise ValueError(f"{field.replace('_', ' ').title()} is required.")

        if pricing_model not in PRICING_MODELS:
            raise ValueError(f"Pricing model must be one of: {', '.join(PRICING_MODELS)}.")

        currency = currency.strip().upper()
        if len(currency) != 3 or not currency.isalpha():
            raise ValueError("Currency must be a three-letter code, such as USD.")

        return cls(
            prospect_id=str(uuid4()),
            name=cleaned["name"],
            company=cleaned["company"],
            niche=cleaned["niche"],
            main_pain=main_pain.strip() or "Follow-up may be inconsistent.",
            desired_outcome=desired_outcome.strip() or "More reliable lead follow-up.",
            pricing_model=pricing_model,
            setup_fee=parse_amount(setup_fee),
            monthly_fee=parse_amount(monthly_fee),
            currency=currency,
            stage="new",
            created_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Prospect":
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
