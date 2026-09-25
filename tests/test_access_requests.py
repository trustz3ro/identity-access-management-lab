import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts/python"))
from evaluate_access_requests import evaluate, read_csv, USER_HEADERS, ROLE_HEADERS, MEMBERSHIP_HEADERS  # noqa: E402


class AccessRequestPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.users = read_csv(ROOT / "data/sample-users.csv", USER_HEADERS)
        cls.roles = read_csv(ROOT / "data/rbac-roles.csv", ROLE_HEADERS)
        cls.memberships = read_csv(ROOT / "data/group-memberships.csv", MEMBERSHIP_HEADERS)

    def request(self, username="jlee", group="GG-Server-Admins", security="Approved"):
        return {
            "request_id": "REQ-TEST", "username": username, "group_name": group,
            "business_reason": "Scheduled server maintenance", "manager_approval": "Approved",
            "owner_approval": "Approved", "security_approval": security,
        }

    def test_privileged_access_requires_security_approval(self):
        without_group = [m for m in self.memberships if not (m["username"] == "jlee" and m["group_name"] == "GG-Server-Admins")]
        pending = evaluate(self.users, self.roles, without_group, [self.request(security="Pending")])
        approved = evaluate(self.users, self.roles, without_group, [self.request()])
        self.assertEqual(pending[0]["decision"], "Pending")
        self.assertEqual(approved[0]["decision"], "Approve")
        self.assertEqual(approved[0]["proposed_action"], "Add group after verification")

    def test_approval_cannot_override_role_or_departure(self):
        outside_role = evaluate(self.users, self.roles, self.memberships, [self.request("mreed")])
        departing = evaluate(self.users, self.roles, self.memberships, [self.request("djames", "GG-All-Employees")])
        self.assertEqual(outside_role[0]["decision"], "Escalate")
        self.assertEqual(departing[0]["decision"], "Reject")


if __name__ == "__main__":
    unittest.main()
