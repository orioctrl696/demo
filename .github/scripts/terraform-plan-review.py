#!/usr/bin/env python3
"""Convert terraform show -json output into a reviewer-friendly PR report."""

import argparse
import json
from pathlib import Path


def action_for(change):
    actions = change.get("actions", [])
    if "delete" in actions and "create" in actions:
        return "Replace"
    if "delete" in actions:
        return "Destroy"
    if "create" in actions:
        return "Create"
    if "update" in actions:
        return "Update"
    return ", ".join(actions) or "No-op"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan-json", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--summary-output", required=True)
    parser.add_argument("--commit-sha", required=True)
    parser.add_argument("--pr-number", required=True)
    args = parser.parse_args()

    plan = json.loads(Path(args.plan_json).read_text())
    counts = {"Create": 0, "Update": 0, "Destroy": 0, "Replace": 0}
    rows = []
    for resource in plan.get("resource_changes", []):
        action = action_for(resource.get("change", {}))
        counts[action] = counts.get(action, 0) + 1
        details = resource.get("change", {}).get("actions", [])
        rows.append((resource.get("address", "unknown"), action, ", ".join(details) or "No-op"))

    lines = [
        "## Terraform Change Review",
        "",
        f"PR: `{args.pr_number}`  |  Commit: `{args.commit_sha}`",
        "",
        "| Resource | Action | Change details |",
        "| --- | --- | --- |",
    ]
    lines.extend(f"| `{address}` | **{action}** | {details} |" for address, action, details in rows)
    lines.extend([
        "",
        "### Summary",
        "",
        f"- Create: **{counts['Create']}**",
        f"- Update: **{counts['Update']}**",
        f"- Destroy: **{counts['Destroy']}**",
        f"- Replace: **{counts['Replace']}**",
        "",
        "Terraform Apply is blocked until this PR is approved. Destroy count above 5 requires the protected manual approval environment.",
    ])
    Path(args.output).write_text("\n".join(lines) + "\n")
    Path(args.summary_output).write_text(
        f"CREATE_COUNT={counts['Create']}\nUPDATE_COUNT={counts['Update']}\n"
        f"DESTROY_COUNT={counts['Destroy']}\nREPLACE_COUNT={counts['Replace']}\n"
    )


if __name__ == "__main__":
    main()