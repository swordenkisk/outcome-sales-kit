# Outcome Sales Kit

A local command-line toolkit for organizing prospects and preparing
outcome-focused GoHighLevel demo plans.

The tool helps you sell a business outcome—such as more consistent lead
follow-up—instead of presenting a CRM feature list. It does not connect to
GoHighLevel, send messages, or call an AI provider.

## Requirements

- Python 3.11 or later
- A POSIX-style shell for `scripts/setup.sh`
- No external Python runtime dependencies

## Setup

From the repository root:

```sh
chmod +x scripts/setup.sh
./scripts/setup.sh
. .venv/bin/activate
The setup script creates .venv if needed and installs this package in
editable mode.

Configuration and data
The application stores prospects as JSON in ./data/prospects.json by
default. The data directory is local to the machine and should be backed up
if its records matter to you.

Use --data-dir before the command to choose a different directory:

sh


outcome-sales --data-dir ./private-sales-data list
Prices are entered as decimal amounts. The default currency is USD; provide
a three-letter currency code with --currency to change the label. The tool
does not convert currencies.

Usage
Initialize the data store:

sh


outcome-sales init
Add a prospect:

sh


outcome-sales add \\
  --name "Morgan Smith" \\
  --company "Smith Plumbing" \\
  --niche "plumbing" \\
  --pain "Missed calls are not followed up consistently" \\
  --outcome "More reliable lead follow-up" \\
  --pricing-model retainer \\
  --setup-fee 750 \\
  --monthly-fee 300 \\
  --currency USD
List prospects and copy the ID from the output:

sh


outcome-sales list
Show details or update a prospect's stage:

sh


outcome-sales show PROSPECT\_ID
outcome-sales stage PROSPECT\_ID demo
Generate a Markdown demo plan:

sh


outcome-sales plan PROSPECT\_ID --output plans/prospect-demo.md
Generate a prompt to paste into an AI tool:

sh


outcome-sales plan PROSPECT\_ID --ai-brief
Supported stages are new, qualified, demo, proposal, won, and
lost. Pricing models are retainer and saas.

Tests
Run the core tests with Python's built-in test runner:

sh


python -m unittest discover -s tests -v
Scope and safety
Demo plans recommend using sample data and test contacts.
The tool does not send messages or make claims about guaranteed results.
Confirm the prospect's actual workflow, implementation scope, costs, and responsibilities before making a proposal.
The AI brief is text for you to copy into a separate AI tool; no API key or external service is configured.
