import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestNotesApp(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health(self):
        r = self.client.get("/healthz")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["status"], "ok")

    def test_crud_notes(self):
        payload = {"title": "hello", "content": "world"}
        r = self.client.post("/notes", json=payload)
        self.assertEqual(r.status_code, 201)
        created = r.json()
        note_id = created["id"]

        r = self.client.get("/notes")
        self.assertEqual(r.status_code, 200)
        self.assertTrue(any(n["id"] == note_id for n in r.json()))

        r = self.client.get(f"/notes/{note_id}")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["title"], "hello")

        r = self.client.put(f"/notes/{note_id}", json={"content": "world!!"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["content"], "world!!")

        r = self.client.delete(f"/notes/{note_id}")
        self.assertEqual(r.status_code, 204)

        r = self.client.get(f"/notes/{note_id}")
        self.assertEqual(r.status_code, 404)

    def test_validation(self):
        r = self.client.post("/notes", json={"title": "", "content": ""})
        self.assertEqual(r.status_code, 422)

if __name__ == "__main__":
    unittest.main()

