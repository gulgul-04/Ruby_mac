import ruby_tools
import ruby_keymap
import llm_client


def test_integration_match_and_info(monkeypatch):
    # Prevent speech and slow calls
    monkeypatch.setattr(ruby_tools, "ruby_speak", lambda *a, **k: None)
    monkeypatch.setattr(ruby_tools, "countdown", lambda *a, **k: None)

    # Ensure match_command finds a direct mapping
    cmd = ruby_keymap.match_command("please tell me system info", use_llama=False)
    assert cmd == "get_system_info"

    info = ruby_tools.get_system_info()
    assert isinstance(info, dict)
    assert "OS" in info
