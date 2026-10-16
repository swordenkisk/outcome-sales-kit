from __future__ import annotations

from outcome_sales_kit.models import Prospect


def build_demo_plan(prospect: Prospect) -> str:
    """Create a prospect-specific demo plan without inventing performance claims."""
    return f"""# Demo plan: {prospect.company}

## Prospect snapshot
- Contact: {prospect.name}
- Business type: {prospect.niche}
- Main concern: {prospect.main_pain}
- Desired outcome: {prospect.desired_outcome}
- Current sales stage: {prospect.stage}

## Suggested discovery questions
1. What happens today when a new lead calls or submits a form?
2. How quickly does someone usually follow up?
3. What happens when a call is missed or the team is busy?
4. How do customers book appointments today?
5. How do you currently ask satisfied customers for reviews?
6. What would make a first month of setup feel successful?

## Demo preparation
Build a demo sub-account with sample data. Do not connect live customer data
or send messages to real customers without the prospect's approval.

1. Create a pipeline with stages that match how {prospect.company} handles leads.
2. Add a booking calendar using the prospect's actual appointment process.
3. Demonstrate a missed-call text-back using a clearly labeled test contact.
4. Demonstrate a review-request workflow with a test contact.
5. Show the prospect where staff can see new leads and their follow-up status.

## Demo talk track
Start with the prospect's process, not a software feature list. Ask permission
to show a sample lead moving through the workflow. Explain what the system
would do, what staff would still need to do, and which settings require the
prospect's input.

Use this framing: "The goal is to make follow-up more consistent and reduce
the chance that an inquiry gets overlooked. Let's map that to your process."

## Offer
- Pricing model: {prospect.pricing_model}
- Setup fee: {prospect.setup_fee} {prospect.currency}
- Monthly fee: {prospect.monthly_fee} {prospect.currency}
- Scope to confirm: setup tasks, included support, message costs, integrations,
  account ownership, cancellation terms, and responsibilities.

Do not promise a particular number of leads, bookings, revenue, or reviews.
Agree on measurable baseline metrics with the prospect before making claims.

## Timeline
- Month 1: confirm requirements, configure the account, test workflows, and train users.
- Month 2: review the agreed metrics, identify issues, and adjust the process.

Present this as a proposed rollout plan, not a guaranteed outcome.

## Next step
Agree on one concrete action: confirm the workflow requirements, schedule a
technical review, or approve a written scope and proposal.
"""


def build_ai_brief(prospect: Prospect) -> str:
    """Create a copyable prompt for an AI tool; this app does not call an AI API."""
    return f"""Help me prepare an ethical, specific sales demo plan for this prospect.

Use only the facts provided below. Do not invent business metrics, ROI, customer
quotes, capabilities, or guarantees. Clearly label recommendations as
recommendations. Keep the language in professional English and focus on
business outcomes rather than selling software features.

Prospect:
- Contact: {prospect.name}
- Company: {prospect.company}
- Niche: {prospect.niche}
- Main pain: {prospect.main_pain}
- Desired outcome: {prospect.desired_outcome}
- Pricing model: {prospect.pricing_model}
- Setup fee: {prospect.setup_fee} {prospect.currency}
- Monthly fee: {prospect.monthly_fee} {prospect.currency}

Include discovery questions, a demo sequence using a test sub-account, risks
to validate before implementation, and a realistic month-one/month-two
rollout. Do not claim that results are guaranteed.
"""
