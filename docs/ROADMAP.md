# IAM Lab Roadmap

This roadmap breaks the project into practical phases so the repository develops like a real identity and access management implementation rather than a one-time lab.

## Phase 1 — Active Directory Foundation
- Build a Windows Server lab environment.
- Install Active Directory Domain Services (AD DS).
- Create a lab domain.
- Create organizational units (OUs) for users, groups, and departments.
- Create sample user accounts and security groups.
- Document the environment with screenshots.

## Phase 2 — Role-Based Access Control
- Map business roles to security groups.
- Apply least-privilege principles.
- Validate access for standard users, managers, privileged users, and IT administrators.
- Record test results and access decisions.

## Phase 3 — Joiner / Mover / Leaver Lifecycle
- Provision a new employee account.
- Assign access based on job role.
- Change access when an employee transfers departments.
- Disable and deprovision access when an employee leaves.
- Document each lifecycle event.

## Phase 4 — Access Reviews and Governance
- Perform a mock quarterly access review.
- Identify excessive or outdated permissions.
- Document approvals, removals, and remediation actions.
- Demonstrate separation of duties and least privilege.

## Phase 5 — Automation
- Use PowerShell to create and manage users and groups.
- Add Python scripts for identity data validation and reporting.
- Track changes through GitHub commits and issues.

## Phase 6 — Cloud IAM Extension
- Extend the project into Microsoft Entra ID or another cloud IAM platform.
- Compare on-premises AD roles with cloud identities and groups.
- Add MFA, conditional access concepts, and privileged role management.

## Phase 7 — Enterprise IAM / IGA Extension
- Model identity governance workflows similar to SailPoint or comparable IGA platforms.
- Add access requests, approvals, certifications, and policy checks.
- Document how the lab maps to real enterprise IAM processes.

## Skills Demonstrated
Active Directory, IAM, RBAC, least privilege, identity lifecycle management, access reviews, access governance, PowerShell, Python, Microsoft Entra ID concepts, separation of duties, documentation, and Git/GitHub workflow.
