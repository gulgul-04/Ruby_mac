import builtins
import io
import os
import time
import importlib
import pytest

import ruby_tools


def test_get_system_info_structure():
    info = ruby_tools.get_system_info()
    # Basic keys should always be present
    assert "OS" in info
    assert "Hostname" in info
    assert "Local IP" in info


def test_countdown_with_numeric(monkeypatch):
    calls = []

    def fake_speak(msg, pause=0):
        calls.append(msg)

    monkeypatch.setattr(ruby_tools, "ruby_speak", fake_speak)
    # avoid actually sleeping
    monkeypatch.setattr(time, "sleep", lambda s: None)

    ruby_tools.countdown("3")
    # expect countdown messages including "Time's up!"
    assert any("Time's up" in c for c in calls) or any("Time's up" in c for c in calls)


def test_take_note_new_session_and_write(monkeypatch, tmp_path):
    # Change cwd to tmp_path so files are written there
    monkeypatch.chdir(tmp_path)

    inputs = iter(["y", "my_notes", "hello world"])  # start new session -> filename -> note
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))

    # prevent speaking side-effects
    monkeypatch.setattr(ruby_tools, "ruby_speak", lambda *a, **k: None)

    ruby_tools.take_note()

    # check file created
    target = tmp_path / "my_notes.txt"
    assert target.exists()
    content = target.read_text(encoding="utf-8")
    assert "hello world" in content


def test_del_files(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    # create a file to delete
    fname = tmp_path / "todelete.txt"
    fname.write_text("remove me")

    inputs = iter(["todelete", "y"])  # filename, confirm
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))
    monkeypatch.setattr(ruby_tools, "ruby_speak", lambda *a, **k: None)

    ruby_tools.del_files()
    assert not fname.exists()


def test_take_note_continuing_session(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    inputs = iter(["n", "a quick note"])  # continue, note
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))
    monkeypatch.setattr(ruby_tools, "ruby_speak", lambda *a, **k: None)

    ruby_tools.take_note()
    notes = tmp_path / "notes.txt"
    assert notes.exists()
    assert "a quick note" in notes.read_text(encoding="utf-8")
