# Identity & Access Management Lab

Hands-on Identity and Access Management (IAM) portfolio project focused on identity lifecycle management, role-based access control (RBAC), least privilege, access reviews, and practical automation.

## Project Objective

Build and document a small enterprise-style IAM environment that demonstrates how organizations manage identities from onboarding through role changes and offboarding.

This lab is designed to demonstrate practical knowledge of:

- Identity lifecycle management
- Joiner, Mover, Leaver (JML) processes
- Role-Based Access Control (RBAC)
- Least privilege
- Group-based access
- Access reviews and recertification
- Separation of duties
- Account provisioning and deprovisioning
- IAM documentation and governance
- PowerShell and Python automation

## Business Scenario

The lab models a fictional company called **TrustZero Solutions**. Employees work in several departments and require different levels of access based on their job responsibilities.

The IAM process must ensure that:

1. New employees receive only the access required for their role.
2. Employees changing jobs have outdated access removed before new access is granted.
3. Departing employees are disabled and deprovisioned promptly.
4. Privileged access is tightly controlled.
5. Access is reviewed periodically.
6. IAM actions are documented for auditability.

## Planned Lab Environment

| Component | Purpose |
|---|---|
| Windows Server / Active Directory | Identity directory and group management |
| Windows client | Test user authentication and access |
| PowerShell | User/group provisioning and lifecycle automation |
| Python | IAM data validation and reporting automation |
| CSV data | Sample HR identity source |
| GitHub | Documentation, scripts, evidence, and version control |

## Repository Structure

```text
identity-access-management-lab/
├── README.md
├── docs/
│   ├── architecture.md
│   ├── rbac-matrix.md
│   ├── joiner-mover-leaver.md
│   └── access-review.md
├── scripts/
│   ├── powershell/
│   └── python/
├── data/
│   └── sample-users.csv
└── evidence/
    └── README.md
```

## Roles Used in the Lab

Initial roles include:

- Help Desk Analyst
- Security Analyst
- HR Specialist
- Finance Analyst
- IT Administrator

Each role is mapped to approved security groups and application permissions. The detailed access model is documented in [`docs/rbac-matrix.md`](docs/rbac-matrix.md).

## IAM Lifecycle Scenarios

### Joiner
A new employee is hired. IAM receives approved identity data from HR, creates the account, assigns baseline access, and adds only the role-specific groups required for the employee's job.

### Mover
An existing employee transfers to another department. Old role access is reviewed and removed before new role permissions are assigned.

### Leaver
An employee leaves the organization. The account is disabled, privileged and group memberships are removed, active sessions are revoked where applicable, and the deprovisioning action is documented.

## Security Principles Demonstrated

### Least Privilege
Users receive the minimum access required to perform assigned duties.

### Role-Based Access Control
Access is granted through predefined business roles instead of assigning permissions individually whenever possible.

### Separation of Duties
High-risk permissions are separated so one individual does not control an entire sensitive business process.

### Access Recertification
Managers and system owners periodically review user access and confirm that permissions are still required.

## Project Roadmap

- [x] Create repository and project structure
- [x] Define IAM business scenario
- [x] Create initial RBAC model
- [x] Document Joiner/Mover/Leaver workflow
- [ ] Build Active Directory lab environment
- [ ] Create organizational units and security groups
- [ ] Provision sample users
- [ ] Test role-based permissions
- [ ] Automate user provisioning with PowerShell
- [ ] Build Python access-review report
- [ ] Capture screenshots and validation evidence
- [ ] Document findings and lessons learned

## Skills Demonstrated

`Identity and Access Management` · `IAM` · `RBAC` · `Active Directory` · `PowerShell` · `Python` · `Least Privilege` · `Access Governance` · `Identity Lifecycle Management` · `Security Administration`

## Author

**Edward Johnson**  
Cybersecurity Technology Student | Cloud & Cybersecurity  
GitHub: [trustz3ro](https://github.com/trustz3ro)

---

> This repository is a controlled educational lab. All users, organizations, credentials, and business data used in the project are fictional.