import unittest
from unittest.mock import patch

import app as honeypot


class HoneypotAppTests(unittest.TestCase):
    def setUp(self):
        honeypot.attack_logs.clear()
        honeypot.blocked_ips.clear()
        honeypot.failed_attempts.clear()
        self.client = honeypot.app.test_client()
        self.clock = [1000.0]
        self.monotonic_patch = patch(
            "app.time.monotonic", side_effect=lambda: self.clock[0]
        )
        self.monotonic_patch.start()
        self.addCleanup(self.monotonic_patch.stop)

    def post_login(self, username="learner@example.test", password="incorrect"):
        return self.client.post(
            "/secret-admin-portal",
            data={"username": username, "password": password},
        )

    def test_ordinary_failed_login_is_logged_with_reason_without_password(self):
        self.post_login(password="classroom-secret")

        self.assertEqual(len(honeypot.attack_logs), 1)
        log_entry = honeypot.attack_logs[0]
        self.assertEqual(log_entry["threat"], "⚠️ Failed Login")
        self.assertEqual(
            log_entry["reason"], "Failed login; no demo detection rule matched."
        )
        self.assertNotIn("password", log_entry)

        dashboard = self.client.get("/dashboard")
        self.assertIn(b"Failed login; no demo detection rule matched.", dashboard.data)
        self.assertNotIn(b"classroom-secret", dashboard.data)

    def test_signature_match_is_blocked_and_explained(self):
        response = self.post_login(username="admin OR 1=1")

        self.assertEqual(response.status_code, 200)
        self.assertIn("SQL injection demo signature matched", honeypot.attack_logs[0]["reason"])
        self.assertIn("SQL injection demo signature matched", honeypot.blocked_ips["127.0.0.1"]["reason"])

    def test_four_failures_in_window_trigger_temporary_quarantine(self):
        for _ in range(honeypot.RATE_LIMIT_MAX_ATTEMPTS):
            response = self.post_login()

        self.assertIn(b"temporary block for 60 seconds", response.data)
        self.assertEqual(len(honeypot.attack_logs), 4)
        self.assertIn("Rate limit exceeded", honeypot.attack_logs[0]["reason"])

        self.clock[0] += honeypot.RATE_LIMIT_BLOCK_SECONDS + 1
        page = self.client.get("/secret-admin-portal")
        self.assertEqual(page.status_code, 200)
        self.assertNotIn("127.0.0.1", honeypot.blocked_ips)

    def test_attempts_outside_window_do_not_accumulate(self):
        for _ in range(honeypot.RATE_LIMIT_MAX_ATTEMPTS - 1):
            self.post_login()

        self.clock[0] += honeypot.RATE_LIMIT_WINDOW_SECONDS + 1
        self.post_login()

        self.assertNotIn("127.0.0.1", honeypot.blocked_ips)
        self.assertEqual(honeypot.attack_logs[0]["attempt"], 1)


if __name__ == "__main__":
    unittest.main()
