import unittest

from outcome_sales_kit.models import Prospect
from outcome_sales_kit.sales import build_ai_brief, build_demo_plan


def make_prospect() -> Prospect:
    return Prospect.create(
        name="Alex Rivera",
        company="Rivera Plumbing",
        niche="plumbing",
        main_pain="Missed calls go unanswered.",
        desired_outcome="More consistent follow-up.",
        pricing_model="retainer",
        setup_fee="500",
        monthly_fee="250",
        currency="USD",
    )


class SalesPlanTests(unittest.TestCase):
    def test_demo_plan_uses_prospect_details(self) -> None:
        plan = build_demo_plan(make_prospect())
        self.assertIn("Rivera Plumbing", plan)
        self.assertIn("Missed calls go unanswered.", plan)
        self.assertIn("500.00 USD", plan)
        self.assertIn("Do not promise", plan)

    def test_ai_brief_is_contextual_and_avoids_guarantees(self) -> None:
        brief = build_ai_brief(make_prospect())
        self.assertIn("Rivera Plumbing", brief)
        self.assertIn("Do not invent business metrics", brief)
        self.assertIn("Do not claim that results are guaranteed", brief)


if __name__ == "__main__":
    unittest.main()
