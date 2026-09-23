# Joiner, Mover, Leaver Workflow

The Joiner/Mover/Leaver (JML) process controls identity access throughout an employee lifecycle and prevents stale or excessive permissions.

## Automated Implementation

The lab uses these files:

- `data/jml-events.csv` — approved lifecycle requests
- `data/sample-users.csv` — authoritative identity records
- `data/rbac-roles.csv` — approved role-to-group mappings
- `data/group-memberships.csv` — current simulated access
- `scripts/python/generate_jml_plan.py` — validation and action-plan logic
- `reports/jml-action-plan.csv` — generated audit evidence

Run the generator from the repository root:

```bash
python3 scripts/python/generate_jml_plan.py
```

The generator is intentionally non-destructive. It validates approved requests and produces an implementation plan before any identity or access changes occur.

## Implemented Test Scenarios

| Event | Scenario | Planned result |
|---|---|---|
| Joiner | Provision Casey Rivers as a Security Analyst | Create and enable the account, place it in the Security OU, and assign baseline and Security groups. |
| Mover | Transfer Avery Collins from Help Desk Analyst to Security Analyst | Remove obsolete Help Desk access before adding Security access and update the department, title, and OU. |
| Leaver | Deprovision departing Finance Analyst Dakota James | Disable the account, revoke sessions, remove all Finance groups, and move the account to Disabled Users. |

## Joiner Controls

1. Require an approved HR reference and effective date.
2. Reject duplicate employee IDs or usernames.
3. Validate the target department and job title against the RBAC model.
4. Calculate baseline and role-specific groups.
5. Require separate review when the target role is privileged.

## Mover Controls

1. Confirm the employee and current role match authoritative identity data.
2. Calculate access to remove from the former role.
3. Calculate acess to add for the new role.
4. Remove obsolete permissions before granting new access.
5. Reassess privileged access rather than carrying it forward.

This prevents privilege creep during transfers.

## Leaver Controls

1. Confirm the employee and current role.
2. Disable the account and revoke active sessions.
3. Remove every current group membership.
4. Move the account to the Disabled Users OU.
5. Transfer owned business resources and retain audit evidence.

## Sample Result

```text
JML PLAN COMPLETED: 3 lifecycle events reviewed.
- Ready: 3
- Invalid: 0
```

## Continuous Validation

GitHub Actions runs the identity validator, RBAC access review, and JML action-plan generator on pushes and pull requests. The workflow uploads `jml-action-plan` as an artifact retained for 30 days.

## Active Directory Extension

The generated plan is the approval and validation layer. A later PowerShell phase will execute the approved actions in the Windows Server Active Directory lab and capture screenshots and command evidence.

## Risks Addressed

- Unauthorized or premature provisioning
- Orphaned accounts
- Excessive permissions
- Privilege creep
- Delayed deprovisioning
- Insider-risk exposure
- Incomplete audit evidence
