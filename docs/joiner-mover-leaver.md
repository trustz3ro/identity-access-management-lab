# Joiner, Mover, Leaver Workflow

The Joiner/Mover/Leaver (JML) process controls identity access throughout an employee's lifecycle.

## Joiner Workflow

1. HR submits approved employee identity data.
2. IAM validates required fields such as name, department, manager, title, and start date.
3. A unique user account is created.
4. The user is placed in the correct Organizational Unit.
5. Baseline employee access is assigned.
6. Role-specific security groups are assigned using the RBAC matrix.
7. Privileged access, if required, follows a separate approval process.
8. The account is tested and provisioning is documented.

### Joiner Validation

- Correct username convention
- Correct department and role
- Correct group memberships
- No unnecessary privileged groups
- Account enabled on approved start date

## Mover Workflow

1. HR or management submits an approved role-change request.
2. IAM identifies the user's existing role and access.
3. Old role-specific access is reviewed and removed.
4. New role-specific access is assigned according to the RBAC matrix.
5. Privileged permissions are reassessed rather than automatically retained.
6. The final access state is validated and documented.

### Key Control

A mover should not simply accumulate access. Outdated permissions must be removed to prevent privilege creep.

## Leaver Workflow

1. HR confirms the employee's separation date/time.
2. IAM disables the account promptly.
3. Active role and privileged group memberships are removed.
4. Remote or application access is revoked where applicable.
5. The account is moved to the Disabled Users OU.
6. Ownership of business data or resources is transferred if required.
7. Deprovisioning actions are documented for audit purposes.

## Risk Addressed

A strong JML process reduces:

- Unauthorized access
- Orphaned accounts
- Excessive permissions
- Privilege creep
- Insider-risk exposure
- Audit findings

## Planned Lab Tests

The lab will test at least three scenarios:

- **Joiner:** Provision a new Security Analyst.
- **Mover:** Transfer a Help Desk Analyst into the Security team and remove obsolete Help Desk access.
- **Leaver:** Disable and deprovision a departing Finance Analyst.

Screenshots and command output from these tests will be stored in the `evidence/` folder.