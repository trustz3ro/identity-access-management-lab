# Access Review and Recertification

## Purpose

Access reviews verify that users still require their assigned permissions. This lab compares current group memberships with the approved RBAC model to identify excessive access, missing access, direct assignments, privileged access, and stale access for departing identities.

## Automated Implementation

The review uses these files:

- `data/sample-users.csv` — authoritative sample identity records
- `data/rbac-roles.csv` — approved job-title-to-group mappings
- `data/group-memberships.csv` — simulated current group memberships
- `scripts/python/generate_access_review.py` — review and reporting logic
- `reports/access-review.csv` — generated certification evidence

Run the review from the repository root:

```bash
python3 scripts/python/generate_access_review.py
```

The script validates its input schemas and flags:

- Missing role-required groups
- Access not authorized by the assigned role
- Direct assignments that should be role-based
- Privileged access outside approved privileged roles
- Departing identities that retain group memberships
- Unknown users, groups, roles, or duplicate memberships

## Review Decisions

- `Approve` — assigned access matches the approved role.
- `Modify` — access or its assignment method requires correction.
- `Revoke` — retained access must be removed.
- `Escalate` — privileged or undefined access requires owner review.

## Sample Review Results

| Decision | Count | Example finding |
|---|---:|---|
| Approve | 4 | Access matches the approved RBAC role. |
| Modify | 1 | Security log access is assigned directly instead of through the role. |
| Revoke | 1 | A departing Finance identity retains active group memberships. |
| Escalate | 0 | No unapproved privileged access was detected. |

## Recertification Workflow

```text
Export Current Access
        |
        v
Compare Role vs RBAC Matrix
        |
        v
Review Exceptions
        |
        v
Approve | Modify | Revoke | Escalate
        |
        v
Implement and Document Changes
```

## Continuous Validation

GitHub Actions validates the identity source, generates the access-review report, and uploads the report as a workflow artifact retained for 30 days. This provides repeatable evidence of basic Identity Governance and Administration (IGA), least-privilege, and access-certification controls.
