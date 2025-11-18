import re
from llm_client import query_llama

# Mapping keywords/phrases to their respective commands/functions
keyword_map = {
    "take_note": [
        "take a note", "make a note", "note down",
        "write down", "remember this", "jot this down"
    ],
    "clear_notes": [
        "clear notes", "delete notes", "erase notes",
        "remove all notes", "reset notes"
    ],
    "open_app": [
        "open app", "launch app", "start app",
        "run app", "execute app"
    ],
    "get_time": [
        "what time is it", "current time", "tell me the time"
    ],
    "countdown": [
        "set timer", "start timer", "countdown", "start countdown"
    ],
    "open_folder": [
        "open folder", "show folder", "explore folder",
        "open directory", "explore directory"
    ],
    "del_files": [
        "delete file", "remove file", "erase file"
    ],
    "get_system_info": [
        "system info", "device info", "system status", "computer info"
    ]
}

def match_command(user_input, use_llama=True):
    """
    Match user input against predefined keyword map.
    If no direct match is found and use_llama is True,
    fallback to querying LLaMA model for command classification.
    Returns the matched command key or None.
    """
    # Normalize input: lowercase and single spaces
    user_input = re.sub(r"\s+", " ", user_input.lower().strip())

    # Check for direct matches with keyword phrases
    for cmd_name, triggers in keyword_map.items():
        for phrase in sorted(triggers, key=len, reverse=True):
            if f" {phrase} " in f" {user_input} ":
                return cmd_name

    # Fallback to LLaMA classifier for unknown commands
    if use_llama:
        prompt = f"""
        You are a command classifier for a virtual assistant.
        User says: "{user_input}"
        Match it to one of these commands: {list(keyword_map.keys())}.
        Respond with only the command key (e.g., 'get_time') or 'unknown'.
        """
        llama_response = query_llama(prompt).strip().lower()
        # Normalize response by replacing spaces and dashes with underscore
        llama_response_normalized = llama_response.replace(" ", "_").replace("-", "_")
        if llama_response_normalized in keyword_map:
            return llama_response_normalized

    # Extra substring check as a last resort
    for key in keyword_map:
        if key.replace("_", " ") in user_input:
            return key

    return None
