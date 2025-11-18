import llm_client


def test_query_llama_returns_unknown_when_no_ollama():
    # If ollama isn't installed, query_llama should return the conservative fallback
    # We don't modify environment; assert the behavior is safe.
    resp = llm_client.query_llama("hello")
    assert isinstance(resp, str)
    # concrete behavior: when ollama missing, implementation returns "unknown"
    if llm_client.ollama is None:
        assert resp == "unknown"
    else:
        # If ollama exists, we at least expect a string
        assert isinstance(resp, str)
