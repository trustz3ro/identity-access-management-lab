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

## Lab Environment

| Component | Purpose |
|---|---|
| Python 3 | Identity validation, RBAC review, JML planning, and access request evaluation (implemented) |
| CSV data | Fictional identity, role, membership, lifecycle, and request inputs (implemented) |
| GitHub Actions | Runs validation and publishes report artifacts (implemented) |
| Windows Server / Active Directory | Directory and group management (planned) |
| PowerShell | Execution of approved lifecycle actions (planned) |

## Repository Structure

```text
identity-access-management-lab/
├── README.md
├── .github/workflows/validate-identities.yml
├── data/ (identities, roles, memberships, JML events, access requests)
├── docs/
│   ├── architecture.md
│   ├── rbac-matrix.md
│   ├── joiner-mover-leaver.md
│   ├── access-review.md
│   └── access-requests.md
├── scripts/python/ (four validators and planners)
├── tests/ (request policy checks)
├── reports/ (generated CSV evidence)
└── evidence/ (run screenshot and walkthrough)
```

## Run the implemented lab

From the repository root with Python 3.12:

```bash
python3 scripts/python/validate_users.py data/sample-users.csv
python3 scripts/python/generate_access_review.py
python3 scripts/python/generate_jml_plan.py
python3 scripts/python/evaluate_access_requests.py
python3 -m unittest discover -s tests
```

The [RBAC access review](reports/access-review.csv) compares current simulated memberships with the approved roles. In the sample data it produces four `Approve`, one `Modify` (a direct assignment), and one `Revoke` (a departing identity retaining access). The [JML action plan](reports/jml-action-plan.csv) produces three `Ready` rows for a joiner, mover, and leaver. The [access request decisions](reports/access-request-decisions.csv) model role and approval checks; see the [request policy](docs/access-requests.md). The [evidence walkthrough](evidence/README.md) explains the earlier inputs, decisions, and [successful workflow run](https://github.com/trustz3ro/identity-access-management-lab/actions/runs/35866986539).

For a concise project summary and resume wording, see [portfolio copy](docs/portfolio-copy.md).

**Scope:** This is a fictional, CSV-backed governance simulation. `Ready` and `Approve` are planning decisions; neither means an account or group changed. The scripts do not connect to Active Directory or execute provisioning, session revocation, or remediation. GitHub Actions runs the checks on pushes and pull requests and uploads the reports for 30 days.

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
- [x] Build Python identity validation, access-review report, and JML action planner
- [x] Model access request decisions and approval checks in Python
- [x] Capture workflow run screenshot and explain generated evidence
- [ ] Capture Active Directory and provisioning screenshots after implementation
- [ ] Document findings and lessons learned

## Skills Demonstrated

`Identity and Access Management` · `RBAC` · `Python` · `GitHub Actions` · `Least Privilege` · `Access Reviews` · `Identity Lifecycle Planning` · `CSV Reporting`

Active Directory and PowerShell execution are planned extensions.

## Author

**Edward Johnson**  
Cybersecurity Technology Student | Cloud & Cybersecurity  
GitHub: [trustz3ro](https://github.com/trustz3ro)

---

> This repository is a controlled educational lab. All users, organizations, credentials, and business data used in the project are fictional.
