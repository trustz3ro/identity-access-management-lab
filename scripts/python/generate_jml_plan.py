#!/usr/bin/env python3

import csv
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

EVENT_HEADERS = [
    "event_id",
    "event_type",
    "effective_date",
    "employee_id",
    "first_name",
    "last_name",
    "username",
    "current_department",
    "current_job_title",
    "new_department",
    "new_job_title",
    "manager",
    "approval_reference",
]

USER_HEADERS = [
    "employee_id",
    "first_name",
    "last_name",
    "username",
    "department",
    "job_title",
    "manager",
    "status",
]

ROLE_HEADERS = [
    "job_title",
    "department",
    "required_groups",
    "privileged_role",
]

MEMBERSHIP_HEADERS = [
    "username",
    "group_name",
    "assignment_type",
    "approval_reference",
]

REPORT_HEADERS = [
    "event_id",
    "event_type",
    "effective_date",
    "employee_id",
    "username",
    "account_action",
    "ou_action",
    "groups_to_add",
    "groups_to_remove",
    "privileged_review",
    "approval_reference",
    "validation_status",
    "notes",
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


def split_groups(value: str) -> set[str]:
    return {group.strip() for group in value.split(";") if group.strip()}


def join_groups(groups: set[str]) -> str:
    return ";".join(sorted(groups))


def validate_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def generate_plan(
    users_path: Path,
    roles_path: Path,
    memberships_path: Path,
    events_path: Path,
    output_path: Path,
) -> int:
    try:
        users = read_csv(users_path, USER_HEADERS)
        roles = read_csv(roles_path, ROLE_HEADERS)
        memberships = read_csv(memberships_path, MEMBERSHIP_HEADERS)
        events = read_csv(events_path, EVENT_HEADERS)
    except ValueError as error:
        print(f"ERROR: {error}")
        return 1

    users_by_id = {user["employee_id"]: user for user in users}
    users_by_username = {user["username"]: user for user in users}
    memberships_by_user = defaultdict(set)
    for membership in memberships:
        memberships_by_user[membership["username"]].add(
            membership["group_name"]
        )

    role_map = {}
    for role in roles:
        role_map[role["job_title"]] = {
            "department": role["department"],
            "groups": split_groups(role["required_groups"]),
            "privileged": role["privileged_role"].lower() == "true",
        }

    seen_event_ids = set()
    report_rows = []
    invalid_events = 0

    for row_number, event in enumerate(events, start=2):
        issues = []
        event_id = event["event_id"]
        event_type = event["event_type"]
        employee_id = event["employee_id"]
        username = event["username"]
        existing_user = users_by_id.get(employee_id)
        actual_groups = memberships_by_user.get(username, set())

        if not event_id:
            issues.append("Event ID is required.")
        elif event_id in seen_event_ids:
            issues.append("Event ID is duplicated.")
        seen_event_ids.add(event_id)

        if event_type not in {"Joiner", "Mover", "Leaver"}:
            issues.append("Event type must be Joiner, Mover, or Leaver.")
        if not validate_date(event["effective_date"]):
            issues.append("Effective date must use YYYY-MM-DD format.")
        if not event["approval_reference"]:
            issues.append("Approval reference is required.")

        account_action = ""
        ou_action = ""
        groups_to_add = set()
        groups_to_remove = set()
        privileged_review = "Not required"
        notes = []

        if event_type == "Joiner":
            if existing_user or username in users_by_username:
                issues.append("Joiner employee ID or username already exists.")
            role = role_map.get(event["new_job_title"])
            if role is None:
                issues.append("New job title has no approved RBAC role.")
            elif event["new_department"] != role["department"]:
                issues.append("New department does not match the RBAC role.")
            else:
                groups_to_add = role["groups"]
                privileged_review = (
                    "Required" if role["privileged"] else "Not required"
                )
            if not all(
                event[field]
                for field in (
                    "employee_id",
                    "first_name",
                    "last_name",
                    "username",
                    "new_department",
                    "new_job_title",
                    "manager",
                )
            ):
                issues.append("Joiner identity and target-role fields are required.")
            account_action = "Create and enable account"
            ou_action = f"Place in OU={event['new_department']}"
            notes.append("Provision baseline and role-based access on approved date.")

        elif event_type == "Mover":
            if existing_user is None or existing_user["username"] != username:
                issues.append("Mover identity does not exist or does not match.")
            else:
                if (
                    existing_user["department"] != event["current_department"]
                    or existing_user["job_title"] != event["current_job_title"]
                ):
                    issues.append("Mover current role does not match identity data.")
            role = role_map.get(event["new_job_title"])
            if role is None:
                issues.append("New job title has no approved RBAC role.")
            elif event["new_department"] != role["department"]:
                issues.append("New department does not match the RBAC role.")
            else:
                groups_to_add = role["groups"] - actual_groups
                groups_to_remove = actual_groups - role["groups"]
                privileged_review = (
                    "Required" if role["privileged"] else "Not required"
                )
            account_action = "Update department and job title"
            ou_action = (
                f"Move from OU={event['current_department']} "
                f"to OU={event['new_department']}"
            )
            notes.append("Remove obsolete access before granting new access.")

        elif event_type == "Leaver":
            if existing_user is None or existing_user["username"] != username:
                issues.append("Leaver identity does not exist or does not match.")
            else:
                if (
                    existing_user["department"] != event["current_department"]
                    or existing_user["job_title"] != event["current_job_title"]
                ):
                    issues.append("Leaver current role does not match identity data.")
            groups_to_remove = actual_groups
            privileged_review = (
                "Required" if "GG-Server-Admins" in actual_groups else "Not required"
            )
            account_action = "Disable account and revoke sessions"
            ou_action = "Move to OU=Disabled Users"
            notes.append("Remove all group memberships and transfer owned resources.")

        validation_status = "Invalid" if issues else "Ready"
        if issues:
            invalid_events += 1
            notes.extend(issues)

        report_rows.append(
            {
                "event_id": event_id,
                "event_type": event_type,
                "effective_date": event["effective_date"],
                "employee_id": employee_id,
                "username": username,
                "account_action": account_action,
                "ou_action": ou_action,
                "groups_to_add": join_groups(groups_to_add),
                "groups_to_remove": join_groups(groups_to_remove),
                "privileged_review": privileged_review,
                "approval_reference": event["approval_reference"],
                "validation_status": validation_status,
                "notes": " ".join(notes),
            }
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=REPORT_HEADERS,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(report_rows)

    ready_events = len(report_rows) - invalid_events
    print(f"JML PLAN COMPLETED: {len(report_rows)} lifecycle events reviewed.")
    print(f"- Ready: {ready_events}")
    print(f"- Invalid: {invalid_events}")
    print(f"Report: {output_path}")
    return 1 if invalid_events else 0


if __name__ == "__main__":
    repository_root = Path(__file__).resolve().parents[2]
    default_paths = [
        repository_root / "data" / "sample-users.csv",
        repository_root / "data" / "rbac-roles.csv",
        repository_root / "data" / "group-memberships.csv",
        repository_root / "data" / "jml-events.csv",
        repository_root / "reports" / "jml-action-plan.csv",
    ]
    selected_paths = [Path(value) for value in sys.argv[1:6]]
    users_file, roles_file, memberships_file, events_file, output_file = (
        selected_paths + default_paths[len(selected_paths):]
    )
    sys.exit(
        generate_plan(
            users_file,
            roles_file,
            memberships_file,
            events_file,
            output_file,
        )
    )
