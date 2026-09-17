# Access Review and Recertification

## Purpose

Access reviews verify that users still require the permissions assigned to them. This helps reduce excessive access, privilege creep, and stale permissions.

## Review Scope

The initial lab review will include:

- Active user accounts
- Department and job role
- Security group memberships
- Privileged access
- Access to sensitive HR and Finance resources
- Accounts with role changes
- Disabled or inactive accounts

## Review Questions

For each identity, the reviewer should confirm:

1. Is the user still active?
2. Is the user's department and role accurate?
3. Does each group membership have a valid business need?
4. Is any privileged access still required?
5. Are there permissions inherited from a previous role?
6. Should any access be removed or modified?

## Sample Review Statuses

- `Approve` — access remains appropriate.
- `Modify` — some access should change.
- `Revoke` — access is no longer required.
- `Escalate` — additional owner or management review is required.

## Recertification Workflow

```text
Export Current Access
        |
        v
Compare Role vs RBAC Matrix
        |
        v
Manager / Owner Review
        |
        v
Approve | Modify | Revoke
        |
        v
Implement Changes
        |
        v
Document Evidence
```

## Planned Automation

A Python script will eventually compare sample identity records against expected role assignments and flag potential exceptions such as:

- Unauthorized group memberships
- Missing required groups
- Privileged access outside approved roles
- Users with access from multiple incompatible roles

The resulting report will provide evidence of basic Identity Governance and Administration (IGA) concepts.