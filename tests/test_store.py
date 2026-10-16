import tempfile
import unittest
from pathlib import Path

from outcome_sales_kit.models import Prospect
from outcome_sales_kit.store import ProspectStore


def make_prospect() -> Prospect:
    return Prospect.create(
        name="Jordan Lee",
        company="Lee Heating",
        niche="HVAC",
        main_pain="Leads are not followed up consistently.",
        desired_outcome="Faster lead response.",
        pricing_model="saas",
        setup_fee="300",
        monthly_fee="199",
        currency="USD",
    )


class ProspectStoreTests(unittest.TestCase):
    def test_add_get_and_update_stage(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = ProspectStore(Path(temp_dir))
            prospect = make_prospect()

            store.add(prospect)
            self.assertEqual(store.get(prospect.prospect_id).company, "Lee Heating")

            updated = store.update_stage(prospect.prospect_id, "demo")
            self.assertEqual(updated.stage, "demo")
            self.assertEqual(store.get(prospect.prospect_id).stage, "demo")

    def test_missing_prospect_raises_key_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = ProspectStore(Path(temp_dir))
            with self.assertRaises(KeyError):
                store.get("missing-id")


if __name__ == "__main__":
    unittest.main()
