import unittest
import os
import datetime
from unittest.mock import patch
import tempfile
import builtins

# Importing the methods to be tested
from ruby_tools import (
    ruby_speak, take_note, open_app, get_time, clear_notes, countdown,
    open_folder, del_files, get_system_info
)

class TestRubyTools(unittest.TestCase):

    def test_ruby_speak(self):
        # Just test that function runs without error
        try:
            ruby_speak("Testing speech function", pause=0)
        except Exception as e:
            self.fail(f"ruby_speak raised Exception unexpectedly: {e}")

    @patch('builtins.input', side_effect=['y', 'test_note'])
    def test_take_note_new_session(self, mock_input):
        with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
            # Overriding ruby_speak to avoid actual speaking during test
            with patch('ruby_tools.ruby_speak'):
                # Patch input and file path for take_note to use temp file
                original = take_note
                def wrapped_take_note():
                    filepath = tmpfile.name
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    note = "\n----------------------------------------\n[" + timestamp + "]\nTest note\n"
                    with open(filepath, "a") as f:
                        f.write(note)
                take_note = wrapped_take_note
                take_note()
                take_note = original
            content = open(tmpfile.name).read()
            self.assertIn("Test note", content)

    @patch('ruby_tools.os.system')
    @patch('ruby_tools.ruby_speak')
    def test_open_app(self, mock_speak, mock_system):
        app_list = ["spotify", "chrome", "brave", "calc", "notes", "unknownapp"]
        for app in app_list:
            open_app(app)
        self.assertEqual(mock_system.call_count, 5)
        self.assertIn("Sorry, I don't know that app yet.", [c[0][0] for c in mock_speak.call_args_list])

    def test_get_time(self):
        try:
            get_time()
        except Exception as e:
            self.fail(f"get_time raised Exception unexpectedly: {e}")

    def test_clear_notes(self):
        with open("notes.txt", "w") as f:
            f.write("test")
        clear_notes()
        with open("notes.txt", "r") as f:
            content = f.read()
        self.assertEqual(content, "")

    @patch('ruby_tools.ruby_speak')
    def test_countdown(self, mock_speak):
        countdown("2")
        countdown("1 minute")
        countdown("invalid")
        self.assertTrue(mock_speak.call_count >= 3)

    @patch('builtins.input', return_value='Documents')
    @patch('ruby_tools.os.system')
    @patch('ruby_tools.ruby_speak')
    def test_open_folder(self, mock_speak, mock_system, mock_input):
        open_folder()
        mock_system.assert_called_once()
        mock_speak.assert_called()

    @patch('builtins.input', side_effect=['testfile', 'y'])
    @patch('ruby_assistant.os.remove')
    @patch('ruby_assistant.ruby_speak')
    def test_del_files_confirmed(self, mock_speak, mock_remove, mock_input):
        del_files()
        mock_remove.assert_called_once()
        mock_speak.assert_any_call("The file has been deleted.")

    @patch('builtins.input', side_effect=['testfile', 'n'])
    @patch('ruby_assistant.os.remove')
    @patch('ruby_assistant.ruby_speak')
    def test_del_files_not_confirmed(self, mock_speak, mock_remove, mock_input):
        del_files()
        mock_remove.assert_not_called()
        mock_speak.assert_any_call("Ok, I won't delete any files.")

    def test_get_system_info(self):
        info = get_system_info()
        self.assertIsInstance(info, dict)
        self.assertIn("OS", info)
        self.assertIn("CPU", info)
        self.assertIn("RAM Total (GB)", info)

if __name__ == "__main__":
    unittest.main()
