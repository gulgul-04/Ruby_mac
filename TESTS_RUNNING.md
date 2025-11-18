Quick test instructions

1) Recommended: create and activate a virtualenv, then install test deps

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Run pytest (preferred)

```bash
python -m pytest -q
```

3) If you don't want to install pytest, run the smoke script which only uses the stdlib:

```bash
python3 tests/run_smoke.py
```

Notes:
- Tests use `pytest` but they avoid side effects by monkeypatching `ruby_tools.ruby_speak` and other slow functions.
- If you see failures related to `pyttsx3` or `psutil`, those packages are optional for runtime and the code falls back to safe behavior.
