
import ruby_tools
import ruby_keymap
from ruby_keymap import match_command
from llm_client import query_llama
#program startup greeting from ruby
ruby_tools.ruby_speak("Hi, I am Ruby, your personal virtual assistant.| Even though i am still a project under progress, how shall i assist you today?")



#the control flow for the several tasks ruby can perfrom.
while True:
    command = input("You: ")
    cmd_name = match_command(command, use_llama=True)
    print(f"[DEBUG] Detected command: {cmd_name}")

    if cmd_name is None:
        # Ask LLaMA to clarify
        prompt = f"""
        The user said: "{command}".
        Which command from {list(ruby_keymap.keyword_map.keys())} best matches this?
        Respond with only the command key or 'unknown'.
        """
        clarified_cmd = query_llama(prompt).strip().lower().replace(" ", "_")
        if clarified_cmd in ruby_keymap.keyword_map:
            cmd_name = clarified_cmd
            ruby_tools.ruby_speak(f"I think you meant '{cmd_name.replace('_', ' ')}'.")
        else:
            ruby_tools.ruby_speak("Sorry, I couldn't understand that.")
            continue  # skip execution if still unknown

    if cmd_name == "take_note":
        ruby_tools.take_note()
    
    elif cmd_name == "clear_notes":
        ruby_tools.ruby_speak("Are you sure you want to clear all notes from notes.txt")
        resp = input("Y/N: ").lower().strip()
        if resp == 'y':
            ruby_tools.clear_notes()
        elif resp == 'n':
            ruby_tools.ruby_speak("Ok, I won't clear notes.")
        else:
            ruby_tools.ruby_speak("Enter a valid input.")
            
    elif cmd_name == "get_time":
        ruby_tools.get_time()

    elif cmd_name == "countdown":
        ruby_tools.ruby_speak("How long should I countdown?")
        secs = input("Duration: ")
        ruby_tools.countdown(secs)

    elif cmd_name == "open_app":
        ruby_tools.ruby_speak("What app would you like for me to open for you?")
        app = input("App: ")
        ruby_tools.open_app(app)

    elif cmd_name == "open_folder":
        ruby_tools.open_folder()

    elif cmd_name == "del_files":
        ruby_tools.del_files()

    elif cmd_name == "get_system_info":
        
        info = ruby_tools.get_system_info()
        print("\n=== System Info ===")
        for k, v in info.items():
            print(f"{k}: {v}")
        print("=====================")

    elif any (kw in command for kw in ["bye", "quit", "exit"]):
        ruby_tools.ruby_speak("Goodbye.")
        break
    else: 
        ruby_tools.ruby_speak("Sorry, I didn't understand that.")
