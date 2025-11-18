import ruby_keymap


def test_direct_match():
    assert ruby_keymap.match_command("please take a note", use_llama=False) == "take_note"
    assert ruby_keymap.match_command("clear notes now", use_llama=False) == "clear_notes"


def test_substring_fallback():
    # key substring present
    assert ruby_keymap.match_command("get system info for me", use_llama=False) == "get_system_info"


def test_llama_fallback(monkeypatch):
    # when use_llama=True, monkeypatch the classifier to return a known command
    monkeypatch.setattr(ruby_keymap, "query_llama", lambda prompt: "take_note")
    assert ruby_keymap.match_command("something ambiguous", use_llama=True) == "take_note"
