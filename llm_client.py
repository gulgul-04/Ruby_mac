import ollama

def query_llama(prompt, model="mistral"):
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )
    return response["message"]["content"].strip()

# Example prompt
result = query_llama("Explain machine learning in simple terms", model="mistral")
print(result)
