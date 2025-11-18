import logging

try:
    import ollama
except ImportError as e:
    ollama = None
    logging.warning(f"ollama module not found: {e}")

def query_llama(prompt: str, model: str = "mistral") -> str:
    """
    Query the local Ollama model if available, otherwise return a safe fallback.

    This function avoids performing network or model calls at import time so the
    rest of the program can import this module safely in environments where
    `ollama` isn't installed or available.

    Args:
        prompt (str): The prompt to send to the model.
        model (str): The name of the model to query (default "mistral").

    Returns:
        str: The model response, or "unknown" if Ollama is not available or on error.
    """
    if ollama is None:
        # Ollama isn't available in this environment; return a conservative fallback.
        logging.error("ollama package is not available.")
        return "unknown"

    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            stream=False
        )
        # Ollama's response expected structure: {"message": {"content": "..."}}
        return response.get("message", {}).get("content", "").strip()
    except (AttributeError, ValueError, ConnectionError) as e:
        logging.error(f"Error querying ollama model: {e}")
        return "unknown"
    except Exception as e:
        # Catch unexpected exceptions but log them for diagnostics
        logging.exception(f"Unexpected error querying ollama model: {e}")
        return "unknown"


if __name__ == "__main__":
    # Example usage when running this module directly.
    if ollama is None:
        print("ollama package not available; example query skipped.")
    else:
        result = query_llama("Explain machine learning in simple terms", model="mistral")
        print(result)
