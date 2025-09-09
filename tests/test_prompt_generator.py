import app.prompt_generator as pg


def test_create_prompt_unknown_provider():
    out = pg.create_prompt("do something", "unknown-provider")
    assert "Unknown provider" in out


def test_create_prompt_llama_success(monkeypatch):
    # Ensure API key present for _require_api_key
    monkeypatch.setenv("TOGETHER_API_KEY", "test-key")
    pg.TOGETHER_API_KEY = "test-key"

    class DummyResp:
        def __init__(self, data):
            self._data = data

        def raise_for_status(self):
            return None

        def json(self):
            return self._data

    def fake_post(url, headers=None, json=None, timeout=None):
        return DummyResp(
            {
                "choices": [
                    {
                        "message": {
                            "content": "TOGETHER DETAILED OK",
                        }
                    }
                ],
            }
        )

    monkeypatch.setattr(pg.requests, "post", fake_post)

    out = pg.create_prompt("write a poem", "llama")
    assert out == "TOGETHER DETAILED OK"



def test_create_short_prompt_llama_success(monkeypatch):
    monkeypatch.setenv("TOGETHER_API_KEY", "test-key")
    pg.TOGETHER_API_KEY = "test-key"

    class DummyResp:
        def __init__(self, data):
            self._data = data

        def raise_for_status(self):
            return None

        def json(self):
            return self._data

    def fake_post(url, headers=None, json=None, timeout=None):
        return DummyResp(
            {
                "choices": [
                    {
                        "message": {
                            "content": "TOGETHER SHORT OK",
                        }
                    }
                ],
            }
        )

    monkeypatch.setattr(pg.requests, "post", fake_post)

    out = pg.create_short_prompt("summarize text", "llama")
    assert out == "TOGETHER SHORT OK"



def test_create_prompt_openai_uses_sdk(monkeypatch):
    class FakeMessage:
        def __init__(self, content):
            self.content = content

    class FakeChoice:
        def __init__(self, content):
            self.message = FakeMessage(content)

    class FakeResponse:
        def __init__(self, content):
            self.choices = [FakeChoice(content)]

    class FakeCompletions:
        def create(self, model, messages, max_tokens=None):
            return FakeResponse("VISION OK")

    class FakeChat:
        def __init__(self):
            self.completions = FakeCompletions()

    class FakeClient:
        def __init__(self):
            self.chat = FakeChat()

    monkeypatch.setattr(pg, "client", FakeClient())
    out = pg.create_prompt("describe an image", "openai")
    assert out == "VISION OK"



def test_create_prompt_gemma_uses_sdk(monkeypatch):
    class FakeMessage:
        def __init__(self, content):
            self.content = content

    class FakeChoice:
        def __init__(self, content):
            self.message = FakeMessage(content)

    class FakeResponse:
        def __init__(self, content):
            self.choices = [FakeChoice(content)]

    class FakeCompletions:
        def create(self, model, messages, max_tokens=None):
            return FakeResponse("GEMMA OK")

    class FakeChat:
        def __init__(self):
            self.completions = FakeCompletions()

    class FakeClient:
        def __init__(self):
            self.chat = FakeChat()

    monkeypatch.setattr(pg, "client", FakeClient())
    out = pg.create_prompt("explain trees", "gemma")
    assert out == "GEMMA OK"
