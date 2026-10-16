from __future__ import annotations

import argparse
import sys
from pathlib import Path

from outcome_sales_kit.models import PRICING_MODELS, STAGES, Prospect
from outcome_sales_kit.sales import build_ai_brief, build_demo_plan
from outcome_sales_kit.store import ProspectStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="outcome-sales",
        description="Track prospects and prepare outcome-focused demo plans.",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data"),
        help="Directory for the local JSON database (default: ./data).",
    )

    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("init", help="Create the local data directory and database.")

    add = commands.add_parser("add", help="Add a prospect.")
    add.add_argument("--name", required=True, help="Prospect contact name.")
    add.add_argument("--company", required=True, help="Business name.")
    add.add_argument("--niche", required=True, help="Business type or niche.")
    add.add_argument("--pain", default="", help="Current follow-up problem.")
    add.add_argument("--outcome", default="", help="Outcome the prospect wants.")
    add.add_argument(
        "--pricing-model",
        choices=PRICING_MODELS,
        default="retainer",
        help="Choose retainer or SaaS-style monthly pricing.",
    )
    add.add_argument("--setup-fee", default="0", help="One-time setup fee.")
    add.add_argument("--monthly-fee", default="0", help="Recurring monthly fee.")
    add.add_argument("--currency", default="USD", help="Three-letter currency code.")

    commands.add_parser("list", help="List saved prospects.")

    show = commands.add_parser("show", help="Show one prospect.")
    show.add_argument("prospect_id")

    stage = commands.add_parser("stage", help="Update a prospect's sales stage.")
    stage.add_argument("prospect_id")
    stage.add_argument("stage", choices=STAGES)

    plan = commands.add_parser("plan", help="Generate a tailored demo plan.")
    plan.add_argument("prospect_id")
    plan.add_argument("--output", type=Path, help="Save the plan to a Markdown file.")
    plan.add_argument(
        "--ai-brief",
        action="store_true",
        help="Print a prompt to paste into an AI tool instead of the demo plan.",
    )

    return parser


def _print_prospect(prospect: Prospect) -> None:
    print(f"ID: {prospect.prospect_id}")
    print(f"Contact: {prospect.name}")
    print(f"Company: {prospect.company}")
    print(f"Niche: {prospect.niche}")
    print(f"Main pain: {prospect.main_pain}")
    print(f"Desired outcome: {prospect.desired_outcome}")
    print(f"Pricing: {prospect.pricing_model}")
    print(f"Setup fee: {prospect.setup_fee} {prospect.currency}")
    print(f"Monthly fee: {prospect.monthly_fee} {prospect.currency}")
    print(f"Stage: {prospect.stage}")
    print(f"Created: {prospect.created_at}")


def run(args: argparse.Namespace) -> int:
    store = ProspectStore(args.data_dir)

    if args.command == "init":
        store.initialize()
        print(f"Initialized local data store at {store.file_path}")
        return 0

    if args.command == "add":
        prospect = Prospect.create(
            name=args.name,
            company=args.company,
            niche=args.niche,
            main_pain=args.pain,
            desired_outcome=args.outcome,
            pricing_model=args.pricing_model,
            setup_fee=args.setup_fee,
            monthly_fee=args.monthly_fee,
            currency=args.currency,
        )
        store.add(prospect)
        print(f"Added {prospect.company}. Prospect ID: {prospect.prospect_id}")
        return 0

    if args.command == "list":
        prospects = store.all()
        if not prospects:
            print("No prospects yet. Add one with the 'add' command.")
            return 0

        for prospect in prospects:
            print(
                f"{prospect.prospect_id} | {prospect.company} | "
                f"{prospect.niche} | {prospect.stage}"
            )
        return 0

    if args.command == "show":
        _print_prospect(store.get(args.prospect_id))
        return 0

    if args.command == "stage":
        prospect = store.update_stage(args.prospect_id, args.stage)
        print(f"Updated {prospect.company} to stage: {prospect.stage}")
        return 0

    if args.command == "plan":
        prospect = store.get(args.prospect_id)
        content = (
            build_ai_brief(prospect)
            if args.ai_brief
            else build_demo_plan(prospect)
        )
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(content, encoding="utf-8")
            print(f"Saved plan to {args.output}")
        else:
            print(content, end="")
        return 0

    return 2


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return run(args)
    except (ValueError, KeyError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
