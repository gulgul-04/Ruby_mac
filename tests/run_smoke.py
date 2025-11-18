"""
Simple smoke test runner that imports the project's modules and calls
some non-interactive functions to surface import-time errors. This does not
require pytest to be installed.
"""
import sys
import traceback
import os

# Ensure parent (project) directory is on sys.path so sibling modules import correctly
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

modules = ["ruby_tools", "ruby_keymap", "llm_client"]
errors = False

for m in modules:
    try:
        mod = __import__(m)
        print(f"Imported {m} OK")
    except Exception:
        print(f"ERROR importing {m}")
        traceback.print_exc()
        errors = True

# call non-interactive functions
try:
    import ruby_tools
    print("Calling get_system_info()...")
    info = ruby_tools.get_system_info()
    print("OK: get_system_info returned keys:", list(info.keys())[:5])
except Exception:
    print("ERROR calling ruby_tools.get_system_info()")
    traceback.print_exc()
    errors = True

try:
    import ruby_keymap
    print("Calling match_command('what time is it', use_llama=False)")
    res = ruby_keymap.match_command('what time is it', use_llama=False)
    print("OK:", res)
except Exception:
    print("ERROR calling ruby_keymap.match_command")
    traceback.print_exc()
    errors = True

try:
    import llm_client
    print("Calling llm_client.query_llama('hello')")
    print("OK:", llm_client.query_llama('hello'))
except Exception:
    print("ERROR calling llm_client.query_llama")
    traceback.print_exc()
    errors = True

if errors:
    sys.exit(1)
print("Smoke checks passed")
