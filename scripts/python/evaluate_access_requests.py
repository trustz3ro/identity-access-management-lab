#!/usr/bin/env python3
"""Evaluate fictional access requests against role and approval policy.

This planner writes decisions only. It never changes group memberships.
"""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
USER_HEADERS = ["employee_id", "first_name", "last_name", "username", "department", "job_title", "manager", "status"]
ROLE_HEADERS = ["job_title", "department", "required_groups", "privileged_role"]
MEMBERSHIP_HEADERS = ["username", "group_name", "assignment_type", "approval_reference"]
REQUEST_HEADERS = ["request_id", "username", "group_name", "business_reason", "manager_approval", "owner_approval", "security_approval"]
REPORT_HEADERS = ["request_id", "username", "group_name", "decision", "reason", "proposed_action"]
PRIVILEGED_GROUPS = {"GG-Server-Admins"}
APPROVAL_VALUES = {"Approved", "Denied", "Pending", "Not Required"}


def read_csv(path, headers):
    with path.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames != headers:
            raise ValueError(f"Invalid headers in {path}: expected {headers}, found {reader.fieldnames}")
        rows = list(reader)
    for number, row in enumerate(rows, start=2):
        if None in row or any(value is None for value in row.values()):
            raise ValueError(f"Malformed row {number} in {path}")
    return [{key: value.strip() for key, value in row.items()} for row in rows]


def evaluate(users, roles, memberships, requests):
    users_by_name = {user["username"]: user for user in users}
    roles_by_title = {role["job_title"]: role for role in roles}
    allowed_groups = {
        group.strip()
        for role in roles
        for group in role["required_groups"].split(";")
        if group.strip()
    }
    current = {(item["username"], item["group_name"]) for item in memberships}
    seen = set()
    results = []

    for request in requests:
        request_id, username, group = (request[key] for key in ("request_id", "username", "group_name"))
        user = users_by_name.get(username)
        role = roles_by_title.get(user["job_title"]) if user else None
        approvals = [request[key] for key in ("manager_approval", "owner_approval", "security_approval")]
        required = approvals[:2] + ([approvals[2]] if group in PRIVILEGED_GROUPS else [])

        if not request_id or request_id in seen:
            decision, reason = "Reject", "Missing or duplicate request ID"
        elif not username or not group or not request["business_reason"]:
            decision, reason = "Reject", "Username, group, and business reason are required"
        elif any(value not in APPROVAL_VALUES for value in approvals):
            decision, reason = "Reject", "Invalid approval state"
        elif user is None:
            decision, reason = "Reject", "Unknown identity"
        elif user["status"] != "Active":
            decision, reason = "Reject", "Identity is not active"
        elif role is None or role["department"] != user["department"]:
            decision, reason = "Reject", "No matching approved business role"
        elif group not in allowed_groups:
            decision, reason = "Reject", "Unknown group"
        elif group not in {g.strip() for g in role["required_groups"].split(";")}:
            decision, reason = "Escalate", "Group falls outside the assigned RBAC role"
        elif (username, group) in current:
            decision, reason = "No change", "Identity already has this group"
        elif "Denied" in required:
            decision, reason = "Reject", "A required approver denied the request"
        elif any(value != "Approved" for value in required):
            decision, reason = "Pending", "Manager, owner, and privileged security approvals must be complete"
        else:
            decision, reason = "Approve", "Within RBAC role; required approvals complete"
        seen.add(request_id)
        results.append({
            "request_id": request_id,
            "username": username,
            "group_name": group,
            "decision": decision,
            "reason": reason,
            "proposed_action": "Add group after verification" if decision == "Approve" else "None",
        })
    return results


def main():
    output = Path(sys.argv[1]) if len(sys.argv) == 2 else ROOT / "reports/access-request-decisions.csv"
    if len(sys.argv) > 2:
        print("Usage: python scripts/python/evaluate_access_requests.py [output.csv]", file=sys.stderr)
        return 2
    try:
        users = read_csv(ROOT / "data/sample-users.csv", USER_HEADERS)
        roles = read_csv(ROOT / "data/rbac-roles.csv", ROLE_HEADERS)
        memberships = read_csv(ROOT / "data/group-memberships.csv", MEMBERSHIP_HEADERS)
        requests = read_csv(ROOT / "data/access-requests.csv", REQUEST_HEADERS)
        results = evaluate(users, roles, memberships, requests)
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", newline="", encoding="utf-8") as target:
            writer = csv.DictWriter(target, fieldnames=REPORT_HEADERS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(results)
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    for result in results:
        print(f"{result['request_id']}: {result['decision']} — {result['reason']}")
    print(f"Report: {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
