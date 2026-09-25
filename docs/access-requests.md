# Access request decision simulation

`python scripts/python/evaluate_access_requests.py` reads fictional identities, RBAC roles, current group memberships, and `data/access-requests.csv`. It writes `reports/access-request-decisions.csv` with one decision per request. **It never grants access.**

The sample requests exercise an out-of-role request, a departing identity, a privileged request outside the assigned role, and a request for access already held. Add a new approved RBAC group that an active user does not yet hold to see an `Approve` decision.

## Decision rules

1. Reject incomplete or duplicate request IDs, missing reasons, unknown identities or groups, and inactive identities.
2. Report `No change` if the user already holds the requested group.
3. Escalate requests outside the user's approved job role. Approval fields cannot override an RBAC mismatch.
4. Require both manager and resource owner approval for eligible requests. Privileged group requests additionally require security approval. Denials are rejected; outstanding approvals remain pending.
5. An approved row is a **proposed** group addition. An operator must verify identity, approvals, and current access before taking action in a live directory.

This is a policy exercise, not a complete IGA platform. Approver identities, signatures, separation of duties, and approval provenance are not independently authenticated by the CSV. The sample users and groups are fictional.
