from fastapi.testclient import TestClient

import app.main as main


client = TestClient(main.app)


def test_root_page_renders():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers.get("content-type", "")


def test_generate_returns_prompt(monkeypatch):
    def fake_create_prompt(task, provider):
        return "PROMPT_OK"

    # Patch the symbol imported into main
    monkeypatch.setattr(main, "create_prompt", fake_create_prompt)

    resp = client.post("/generate", json={"task": "x", "provider": "llama"})
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("prompt") == "PROMPT_OK"


def test_generate_missing_task():
    resp = client.post("/generate", json={"provider": "llama"})
    assert resp.status_code == 200
    assert resp.json().get("error") == "Please provide a 'task'"


def test_generate_missing_provider():
    resp = client.post("/generate", json={"task": "x"})
    assert resp.status_code == 200
    assert resp.json().get("error") == "Please select a 'provider'"


def test_generate_short_returns_prompt(monkeypatch):
    def fake_create_short(task, provider):
        return "SHORT_OK"

    monkeypatch.setattr(main, "create_short_prompt", fake_create_short)

    resp = client.post("/generate-short", json={"task": "x", "provider": "llama"})
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("prompt") == "SHORT_OK"
