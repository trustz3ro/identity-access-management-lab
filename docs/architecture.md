# IAM Lab Architecture

## Overview

This lab models a small enterprise Identity and Access Management environment for **TrustZero Solutions**.

## Identity Flow

```text
HR / Identity Source
        |
        v
IAM Administrator
        |
        v
Active Directory
   |      |      |
   v      v      v
Users   Groups  Roles
   \      |      /
    \     |     /
     v    v    v
 Applications / Shared Resources
```

## Core Components

### Identity Source
A CSV file represents approved HR data for employees entering or changing within the organization.

### Active Directory
Active Directory will be used to create and manage:

- User accounts
- Organizational Units (OUs)
- Security groups
- Role-based access assignments
- Disabled accounts

### Administrative Workstation
A Windows client or management workstation will be used to test authentication, group membership, and administrative workflows.

### Automation
PowerShell will be used for account provisioning and group membership changes. Python will later be used for validation, reporting, and access-review support.

## Proposed Organizational Units

```text
TrustZero Solutions
├── Employees
│   ├── Finance
│   ├── Human Resources
│   ├── IT
│   └── Security
├── Administrators
├── Service Accounts
├── Groups
└── Disabled Users
```

## Access Design

Access will be assigned primarily through security groups mapped to business roles. Direct permission assignments will be avoided unless specifically required and documented.

## Security Controls

- Least privilege
- Role-based access control
- Separation of duties
- Privileged access restriction
- Access recertification
- Prompt deprovisioning
- Audit documentation

## Future Enhancements

- MFA concepts
- Microsoft Entra ID integration
- Hybrid identity architecture
- Privileged Access Management (PAM)
- SailPoint-style identity governance workflows
- Automated access certification reports