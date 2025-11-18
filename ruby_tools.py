import os
import time
import datetime
import platform
import psutil
import socket
import uuid
import pyttsx3

# Function to convert text to speech using pyttsx3 on macOS.
# Speaks the given text with optional pause between segments.
def ruby_speak(text, pause=0):
    engine = pyttsx3.init('nsss')  # Use macOS native speech synthesizer
    # Select a female voice, e.g., Samantha if available
    for voice in engine.getProperty('voices'):
        if "female" in voice.name.lower() or 'samantha' in voice.id:
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 180)  # Set speech rate
    segments = text.split('|')
    for segment in segments:
        cleaned = segment.strip()
        if cleaned:
            engine.say(cleaned)
            engine.runAndWait()
            time.sleep(pause)

# Function to prompt user to take notes and save them to a timestamped text file.
# Can start new session or continue existing notes file.
def take_note():
    ruby_speak("Do you want to start a new session?")
    session = input("Y/N: ").lower().strip()
    if session == 'y':
        ruby_speak("Starting new session.")
        filepath = input("file name: ") + ".txt"
    else:
        ruby_speak("Continuing in existing session.")
        filepath = "notes.txt"

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ruby_speak("What should I write?")
    note = input("Note: ")
    note = f"\n{'-'*40}\n[{timestamp}]\n{note.strip()}\n"

    with open(filepath, "a", encoding="utf-8") as f:
        f.write(note)
        ruby_speak("Note saved.")

# Function to open common applications on macOS based on app name.
# Uses 'open -a' shell command compatible with macOS.
def open_app(app_name):
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
    try:
        open("notes.txt", "w").close()
        ruby_speak("All notes have been cleared.")
    except Exception:
        ruby_speak("I couldn't clear the note.")

# Function to start a countdown for given duration in seconds or minutes.
# Speaks countdown numbers at one second intervals.
def countdown(duration):
    try:
        duration = duration.strip().lower()
        if "minute" in duration:
            number = float(duration.split()[0])
            seconds = int(number * 60)
        else:
            seconds = int(duration)
        ruby_speak(f"Starting countdown for {seconds} seconds now.")
        while seconds > 0:
            print(seconds)
            ruby_speak(str(seconds))
            time.sleep(1)
            seconds -= 1
        print("Time's up!")
        ruby_speak("Time's up!")
    except ValueError:
        ruby_speak("Please enter a valid number.")

# Function to open a user specified folder located in home directory.
# Uses macOS 'open' command for folder navigation.
def open_folder():
    ruby_speak("What folder should I open?")
    folder = input("Folder: ")
    ruby_speak("Opening your folder.")
    user_home = os.path.expanduser("~")
    os.system(f"open '{os.path.join(user_home, folder)}'")

# Function to delete a specified text file after user confirmation.
def del_files():
    ruby_speak("What files do you want me to delete?")
    file = input("File name: ") + ".txt"
    ruby_speak("Are you sure you want to delete this file?")
    resp = input("Y/N: ").lower().strip()
    if resp == 'y':
        try:
            os.remove(file)
            ruby_speak("The file has been deleted.")
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
    info["Cores"] = psutil.cpu_count(logical=True)
    info["CPU Usage %"] = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    info["RAM Total (GB)"] = round(mem.total / (1024**3), 2)
    info["RAM Used (GB)"] = round(mem.used / (1024**3), 2)
    disk = psutil.disk_usage('/')
    info["Disk Total (GB)"] = round(disk.total / (1024**3), 2)
    info["Disk Free (GB)"] = round(disk.free / (1024**3), 2)
    info["Hostname"] = socket.gethostname()
    info["Local IP"] = socket.gethostbyname(socket.gethostname())
    if hasattr(psutil, "sensors_battery"):
        battery = psutil.sensors_battery()
        if battery:
            info["Battery%"] = battery.percent
    return info
