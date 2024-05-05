import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from unittest.mock import patch

class BayardTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_health_check(self):
        print("Running test: test_health_check")
        response = self.app.get("/health-check")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "OK")
        print("Test passed: test_health_check")

    def test_generate_api_key(self):
        print("Running test: test_generate_api_key")
        with patch("app.supabase.table") as mock_table:
            mock_table.return_value.insert.return_value.execute.return_value = True
            response = self.app.get("/api/generate-key")
            self.assertEqual(response.status_code, 200)
            self.assertIn("api_key", response.json)
        print("Test passed: test_generate_api_key")

    def test_bayard_api_missing_input(self):
        print("Running test: test_bayard_api_missing_input")
        response = self.app.post("/api/bayard", json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Input text is required")
        print("Test passed: test_bayard_api_missing_input")

    def test_bayard_api_invalid_api_key(self):
        print("Running test: test_bayard_api_invalid_api_key")
        with patch("app.supabase.table") as mock_table:
            mock_table.return_value.select.return_value.ilike.return_value.execute.return_value.data = []
            response = self.app.post("/api/bayard", json={"input_text": "test"}, headers={"X-API-Key": "invalid_key"})
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json["error"], "Invalid API key")
        print("Test passed: test_bayard_api_invalid_api_key")

    def test_bayard_api_rate_limit_exceeded(self):
        print("Running test: test_bayard_api_rate_limit_exceeded")
        with patch("app.rate_limit") as mock_rate_limit:
            mock_rate_limit.return_value = False
            response = self.app.post("/api/bayard", json={"input_text": "test"}, headers={"X-API-Key": "valid_key"})
            self.assertEqual(response.status_code, 429)
            self.assertEqual(response.json["error"], "Rate limit exceeded")
        print("Test passed: test_bayard_api_rate_limit_exceeded")

if __name__ == "__main__":
    unittest.main()