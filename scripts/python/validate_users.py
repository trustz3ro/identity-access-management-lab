#!/usr/bin/env python3

import csv
import re
import sys
from pathlib import Path

REQUIRED_HEADERS = [
    "employee_id",
    "first_name",
    "last_name",
    "username",
    "department",
    "job_title",
    "manager",
    "status",
]

ROLE_DEPARTMENTS = {
    "Help Desk Analyst": "IT",
    "Security Analyst": "Security",
    "HR Specialist": "Human Resources",
    "Finance Analyst": "Finance",
    "IT Administrator": "IT",
}

VALID_STATUSES = {"Active", "Departing"}


def validate(csv_path: Path) -> int:
    errors = []
    employee_ids = set()
    usernames = set()

    if not csv_path.is_file():
        print(f"ERROR: File not found: {csv_path}")
        return 1

    with csv_path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames != REQUIRED_HEADERS:
            print("ERROR: CSV headers do not match the required schema.")
            print(f"Expected: {REQUIRED_HEADERS}")
            print(f"Found:    {reader.fieldnames}")
            return 1

        rows = list(reader)

    for row_number, row in enumerate(rows, start=2):
        row = {key: value.strip() for key, value in row.items()}

        for field in REQUIRED_HEADERS:
            if not row[field]:
                errors.append(f"Row {row_number}: {field} is required.")

        employee_id = row["employee_id"]
        username = row["username"]
        department = row["department"]
        job_title = row["job_title"]
        status = row["status"]

        if not re.fullmatch(r"TZ\d{4}", employee_id):
            errors.append(
                f"Row {row_number}: invalid employee ID '{employee_id}'."
            )

        if employee_id in employee_ids:
            errors.append(
                f"Row {row_number}: duplicate employee ID '{employee_id}'."
            )
        employee_ids.add(employee_id)

        if not re.fullmatch(r"[a-z][a-z0-9._-]*", username):
            errors.append(
                f"Row {row_number}: invalid username '{username}'."
            )

        if username in usernames:
            errors.append(
                f"Row {row_number}: duplicate username '{username}'."
            )
        usernames.add(username)

        if job_title not in ROLE_DEPARTMENTS:
            errors.append(
                f"Row {row_number}: unapproved job title '{job_title}'."
            )
        elif department != ROLE_DEPARTMENTS[job_title]:
            errors.append(
                f"Row {row_number}: '{job_title}' must belong to "
                f"'{ROLE_DEPARTMENTS[job_title]}', not '{department}'."
            )

        if status not in VALID_STATUSES:
            errors.append(
                f"Row {row_number}: invalid status '{status}'."
            )

    if errors:
        print(f"VALIDATION FAILED: {len(errors)} issue(s) found.")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"VALIDATION PASSED: {len(rows)} identity records are valid.")
    print(f"Source: {csv_path}")
    return 0


if __name__ == "__main__":
    default_file = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "sample-users.csv"
    )
    selected_file = Path(sys.argv[1]) if len(sys.argv) > 1 else default_file
    sys.exit(validate(selected_file))
