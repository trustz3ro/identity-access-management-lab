# Role-Based Access Control Matrix

This matrix defines the initial role model for the TrustZero Solutions IAM lab.

| Role | Department | Standard User | Help Desk Tools | Security Logs | HR Records | Finance Share | Server Admin | Privileged Access |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Help Desk Analyst | IT | Yes | Yes | Read | No | No | No | No |
| Security Analyst | Security | Yes | Limited | Yes | No | No | No | Limited |
| HR Specialist | Human Resources | Yes | No | No | Yes | No | No | No |
| Finance Analyst | Finance | Yes | No | No | No | Yes | No | No |
| IT Administrator | IT | Yes | Yes | Yes | No | No | Yes | Yes |

## Proposed Security Groups

- `GG-All-Employees`
- `GG-HelpDesk-Analysts`
- `GG-Security-Analysts`
- `GG-HR-Specialists`
- `GG-Finance-Analysts`
- `GG-IT-Administrators`
- `GG-Security-Log-Readers`
- `GG-Finance-Share-RW`
- `GG-HR-Records-RW`
- `GG-Server-Admins`

## Access Rules

1. Every employee receives the baseline employee group.
2. Business access is granted by job role through group membership.
3. Direct access assignments should be avoided.
4. Privileged roles require separate approval and documentation.
5. Role changes require removal of obsolete access before granting new access.
6. Terminated users must be removed from all active groups and disabled.
7. Access should be reviewed periodically by the appropriate manager or system owner.

## Separation of Duties Example

A Finance Analyst may access the finance shared resource but does not receive server administration rights. An IT Administrator may administer servers but does not automatically receive access to HR or Finance business records.

This reduces unnecessary privilege and limits the impact of account misuse or compromise.