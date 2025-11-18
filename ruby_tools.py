import os
import time
import datetime
import platform
import socket
import uuid
import shlex

# Optional dependencies: psutil and pyttsx3. Use safe fallbacks when missing.
try:
    import psutil
except Exception:
    psutil = None

try:
    import pyttsx3
except Exception:
    pyttsx3 = None

# Function to convert text to speech using pyttsx3 on macOS.
# Speaks the given text with optional pause between segments.
def ruby_speak(text, pause=0):
    """Speak the given `text`.

    Tries to use `pyttsx3` when available, falls back to the macOS
    `say` command, and finally prints to stdout if neither is available.
    Text may include `|` to separate speaking segments.
    """
    segments = [s.strip() for s in text.split('|') if s.strip()]

    # Prefer pyttsx3 if installed and usable
    if pyttsx3 is not None:
        try:
            engine = pyttsx3.init('nsss')
            # Try to prefer a female voice if available
            try:
                for voice in engine.getProperty('voices'):
                    if "female" in getattr(voice, 'name', '').lower() or 'samantha' in getattr(voice, 'id', '').lower():
                        engine.setProperty('voice', voice.id)
                        break
            except Exception:
                # non-fatal: voice selection may not be supported on all engines
                pass
            engine.setProperty('rate', 180)
            for segment in segments:
                engine.say(segment)
                engine.runAndWait()
                time.sleep(pause)
            return
        except Exception:
            # Fall through to other fallbacks
            pass

    # macOS native `say` command fallback
    try:
        for segment in segments:
            safe = shlex.quote(segment)
            os.system(f"say {safe}")
            time.sleep(pause)
        return
    except Exception:
        pass

    # Last resort: print to console
    for segment in segments:
        print("Ruby says:", segment)
        time.sleep(pause)

# Function to prompt user to take notes and save them to a timestamped text file.
# Can start new session or continue existing notes file.
def take_note():
    """Interactively append a timestamped note to a file.

    If user chooses to start a new session, prompt for filename; otherwise
    append to `notes.txt`.
    """
    ruby_speak("Do you want to start a new session?")
    session = input("Y/N: ").lower().strip()
    if session == 'y':
        ruby_speak("Starting new session.")
        filename = input("file name: ").strip()
        if not filename:
            ruby_speak("No file name given, using notes.txt")
            filepath = "notes.txt"
        else:
            filepath = filename + ".txt"
    else:
        ruby_speak("Continuing in existing session.")
        filepath = "notes.txt"

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ruby_speak("What should I write?")
    note = input("Note: ")
    note = f"\n{'-'*40}\n[{timestamp}]\n{note.strip()}\n"

    try:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(note)
        ruby_speak("Note saved.")
    except Exception:
        ruby_speak("Failed to save note.")

# Function to open common applications on macOS based on app name.
# Uses 'open -a' shell command compatible with macOS.
def open_app(app_name):
    """Open a macOS application by name (best-effort).

    This function is intentionally forgiving and will speak a message
    if it doesn't recognize the requested application.
    """
    app_name = (app_name or "").lower()
    if "spotify" in app_name:
        ruby_speak("Opening Spotify.")
        os.system("open -a Spotify")
    elif "chrome" in app_name:
        ruby_speak("Opening Chrome.")
        os.system("open -a 'Google Chrome'")
    elif "brave" in app_name:
        ruby_speak("Opening Brave.")
        os.system("open -a Brave")
    elif "calc" in app_name or "calculator" in app_name:
        ruby_speak("Opening Calculator.")
        os.system("open -a Calculator")
    elif "notes" in app_name:
        ruby_speak("Opening Notes.")
        os.system("open -a Notes")
    else:
        ruby_speak("Sorry, I don't know that app yet.")

# Function to tell the current system time in 12-hour format.
def get_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    ruby_speak(f"The time is {now}.")

# Function to clear all existing notes by resetting the notes.txt file.
def clear_notes():
    """Clear the default `notes.txt` file contents."""
    try:
        with open("notes.txt", "w", encoding="utf-8"):
            pass
        ruby_speak("All notes have been cleared.")
    except Exception:
        ruby_speak("I couldn't clear the notes.")

# Function to start a countdown for given duration in seconds or minutes.
# Speaks countdown numbers at one second intervals.
def countdown(duration):
    """Start a spoken countdown.

    `duration` may be a number of seconds (string or numeric) or contain the
    word "minute(s)"; e.g. "2 minutes".
    """
    try:
        duration = str(duration).strip().lower()
        if "minute" in duration:
            number = float(duration.split()[0])
            seconds = int(number * 60)
        else:
            seconds = int(float(duration))
        ruby_speak(f"Starting countdown for {seconds} seconds now.")
        while seconds > 0:
            print(seconds)
            ruby_speak(str(seconds))
            time.sleep(1)
            seconds -= 1
        print("Time's up!")
        ruby_speak("Time's up!")
    except Exception:
        ruby_speak("Please enter a valid number.")

# Function to open a user specified folder located in home directory.
# Uses macOS 'open' command for folder navigation.
def open_folder():
    ruby_speak("What folder should I open?")
    folder = input("Folder: ").strip()
    if not folder:
        ruby_speak("No folder provided.")
        return
    ruby_speak("Opening your folder.")
    user_home = os.path.expanduser("~")
    path = os.path.join(user_home, folder)
    safe = shlex.quote(path)
    os.system(f"open {safe}")

# Function to delete a specified text file after user confirmation.
def del_files():
    ruby_speak("What files do you want me to delete?")
    filename = input("File name: ").strip()
    if not filename:
        ruby_speak("No file name given.")
        return
    file = filename + ".txt"
    ruby_speak(f"Are you sure you want to delete {file}?")
    resp = input("Y/N: ").lower().strip()
    if resp == 'y':
        try:
            if os.path.exists(file):
                os.remove(file)
                ruby_speak("The file has been deleted.")
            else:
                ruby_speak("File not found.")
        except Exception:
            ruby_speak("Could not delete the file.")
    else:
        ruby_speak("Ok, I won't delete any files.")

# Function to gather detailed system information including OS, CPU, RAM, disk, network, and battery.
# Useful for diagnostics or reporting system status.
def get_system_info():
    info = {}
    info["OS"] = platform.system()
    info["OS Version"] = platform.version()
    info["Release"] = platform.release()
    info["Machine"] = platform.machine()
    info["CPU"] = platform.processor()
    # Use psutil when available, otherwise use safe fallbacks
    if psutil is not None:
        try:
            info["Cores"] = psutil.cpu_count(logical=True)
            info["CPU Usage %"] = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory()
            info["RAM Total (GB)"] = round(mem.total / (1024**3), 2)
            info["RAM Used (GB)"] = round(mem.used / (1024**3), 2)
            disk = psutil.disk_usage('/')
            info["Disk Total (GB)"] = round(disk.total / (1024**3), 2)
            info["Disk Free (GB)"] = round(disk.free / (1024**3), 2)
        except Exception:
            psutil_fallback(info)
    else:
        psutil_fallback(info)
    info["Hostname"] = socket.gethostname()
    info["Local IP"] = socket.gethostbyname(socket.gethostname())
    if hasattr(psutil, "sensors_battery"):
        battery = psutil.sensors_battery()
        if battery:
            info["Battery%"] = battery.percent
    return info


def psutil_fallback(info: dict):
    """Populate basic system info when psutil is not available."""
    try:
        info["Cores"] = os.cpu_count()
    except Exception:
        info["Cores"] = None
    try:
        # Cannot get CPU percent without psutil; set to None
        info["CPU Usage %"] = None
    except Exception:
        info["CPU Usage %"] = None
    try:
        import shutil
        disk = shutil.disk_usage('/')
        info["Disk Total (GB)"] = round(disk.total / (1024**3), 2)
        info["Disk Free (GB)"] = round(disk.free / (1024**3), 2)
    except Exception:
        info["Disk Total (GB)"] = None
        info["Disk Free (GB)"] = None
    try:
        # RAM info not available without psutil
        info["RAM Total (GB)"] = None
        info["RAM Used (GB)"] = None
    except Exception:
        info["RAM Total (GB)"] = None
        info["RAM Used (GB)"] = None
