#!/usr/bin/env python3

import csv
import sys
from collections import defaultdict
from pathlib import Path

PRIVILEGED_GROUPS = {"GG-Server-Admins"}
VALID_ASSIGNMENT_TYPES = {"Role-Based", "Direct"}
REPORT_HEADERS = [
    "employee_id",
    "username",
    "identity_status",
    "job_title",
    "expected_groups",
    "actual_groups",
    "missing_groups",
    "unauthorized_groups",
    "direct_assignments",
    "privileged_access",
    "review_decision",
    "review_notes",
]


def read_csv(path: Path, required_headers: list[str]) -> list[dict[str, str]]:
    if not path.is_file():
        raise ValueError(f"File not found: {path}")

    with path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != required_headers:
            raise ValueError(
                f"Invalid headers in {path}. "
                f"Expected {required_headers}; found {reader.fieldnames}."
            )
        return [
            {key: value.strip() for key, value in row.items()}
            for row in reader
        ]


def join_values(values: set[str]) -> str:
    return ";".join(sorted(values))


def generate_review(
    users_path: Path,
    roles_path: Path,
    memberships_path: Path,
    output_path: Path,
) -> int:
    user_headers = [
        "employee_id",
        "first_name",
        "last_name",
        "username",
        "department",
        "job_title",
        "manager",
        "status",
    ]
    role_headers = [
        "job_title",
        "department",
        "required_groups",
        "privileged_role",
    ]
    membership_headers = [
        "username",
        "group_name",
        "assignment_type",
        "approval_reference",
    ]

    try:
        users = read_csv(users_path, user_headers)
        roles = read_csv(roles_path, role_headers)
        memberships = read_csv(memberships_path, membership_headers)
    except ValueError as error:
        print(f"ERROR: {error}")
        return 1

    errors = []
    role_map = {}
    known_groups = set()

    for row_number, role in enumerate(roles, start=2):
        job_title = role["job_title"]
        if job_title in role_map:
            errors.append(
                f"{roles_path} row {row_number}: duplicate role '{job_title}'."
            )
            continue

        required_groups = {
            group.strip()
            for group in role["required_groups"].split(";")
            if group.strip()
        }
        if not required_groups:
            errors.append(
                f"{roles_path} row {row_number}: role '{job_title}' has no groups."
            )

        privileged_value = role["privileged_role"].lower()
        if privileged_value not in {"true", "false"}:
            errors.append(
                f"{roles_path} row {row_number}: privileged_role must be true or false."
            )

        role_map[job_title] = {
            "department": role["department"],
            "required_groups": required_groups,
            "privileged_role": privileged_value == "true",
        }
        known_groups.update(required_groups)

    users_by_username = {user["username"]: user for user in users}
    memberships_by_user = defaultdict(list)
    seen_memberships = set()

    for row_number, membership in enumerate(memberships, start=2):
        username = membership["username"]
        group_name = membership["group_name"]
        assignment_type = membership["assignment_type"]
        membership_key = (username, group_name)

        if username not in users_by_username:
            errors.append(
                f"{memberships_path} row {row_number}: unknown username '{username}'."
            )
        if group_name not in known_groups:
            errors.append(
                f"{memberships_path} row {row_number}: unknown group '{group_name}'."
            )
        if assignment_type not in VALID_ASSIGNMENT_TYPES:
            errors.append(
                f"{memberships_path} row {row_number}: invalid assignment type "
                f"'{assignment_type}'."
            )
        if membership_key in seen_memberships:
            errors.append(
                f"{memberships_path} row {row_number}: duplicate membership "
                f"'{username}' -> '{group_name}'."
            )

        seen_memberships.add(membership_key)
        memberships_by_user[username].append(membership)

    if errors:
        print(f"ACCESS REVIEW FAILED: {len(errors)} data issue(s) found.")
        for error in errors:
            print(f"- {error}")
        return 1

    report_rows = []
    decision_counts = defaultdict(int)

    for user in users:
        username = user["username"]
        role = role_map.get(user["job_title"])
        actual_records = memberships_by_user.get(username, [])
        actual_groups = {record["group_name"] for record in actual_records}
        direct_groups = {
            record["group_name"]
            for record in actual_records
            if record["assignment_type"] == "Direct"
        }
        privileged_groups = actual_groups & PRIVILEGED_GROUPS
        notes = []

        if role is None:
            expected_groups = set()
            missing_groups = set()
            unauthorized_groups = actual_groups
            decision = "Escalate"
            notes.append("No approved RBAC role exists for this job title.")
        else:
            expected_groups = role["required_groups"]
            missing_groups = expected_groups - actual_groups
            unauthorized_groups = actual_groups - expected_groups

            if user["department"] != role["department"]:
                notes.append("Department does not match the approved role definition.")

            if user["status"] != "Active":
                decision = "Revoke"
                notes.append("Departing identity retains active group memberships.")
            elif unauthorized_groups or missing_groups:
                decision = "Modify"
            elif direct_groups:
                decision = "Modify"
                notes.append("Replace direct assignments with role-based membership.")
            else:
                decision = "Approve"

            if missing_groups:
                notes.append("Add missing role-required access.")
            if unauthorized_groups:
                notes.append("Remove access not authorized by the assigned role.")
            if privileged_groups and not role["privileged_role"]:
                decision = "Escalate"
                notes.append("Privileged access is not approved for this role.")

        decision_counts[decision] += 1
        report_rows.append(
            {
                "employee_id": user["employee_id"],
                "username": username,
                "identity_status": user["status"],
                "job_title": user["job_title"],
                "expected_groups": join_values(expected_groups),
                "actual_groups": join_values(actual_groups),
                "missing_groups": join_values(missing_groups),
                "unauthorized_groups": join_values(unauthorized_groups),
                "direct_assignments": join_values(direct_groups),
                "privileged_access": join_values(privileged_groups),
                "review_decision": decision,
                "review_notes": " ".join(notes),
            }
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=REPORT_HEADERS)
        writer.writeheader()
        writer.writerows(report_rows)

    print(f"ACCESS REVIEW COMPLETED: {len(report_rows)} identities reviewed.")
    for decision in ("Approve", "Modify", "Revoke", "Escalate"):
        print(f"- {decision}: {decision_counts[decision]}")
    print(f"Report: {output_path}")
    return 0


if __name__ == "__main__":
    repository_root = Path(__file__).resolve().parents[2]
    default_paths = [
        repository_root / "data" / "sample-users.csv",
        repository_root / "data" / "rbac-roles.csv",
        repository_root / "data" / "group-memberships.csv",
        repository_root / "reports" / "access-review.csv",
    ]
    selected_paths = [Path(value) for value in sys.argv[1:5]]
    users_file, roles_file, memberships_file, output_file = (
        selected_paths + default_paths[len(selected_paths):]
    )
    sys.exit(
        generate_review(
            users_file,
            roles_file,
            memberships_file,
            output_file,
        )
    )
