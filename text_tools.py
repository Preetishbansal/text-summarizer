"""
text_tools.py

This is the "tool calling" piece. We define a plain Python function,
decorate it with @tool, and CrewAI exposes it to the Agent as something
the LLM can decide to call when it needs that capability.

The agent doesn't run this code blindly start-to-finish like a normal
script call — the LLM reads the docstring/description, decides IF and
WHEN to call it during its reasoning, passes it arguments, and gets the
result back to use in its final answer.
"""

import re
from crewai.tools import tool


@tool("Text Statistics Analyzer")
def analyze_text_stats(text: str) -> str:
    """
    Analyzes a block of text and returns basic statistics:
    word count, character count, sentence count, and the
    top 5 most frequent words (excluding very short/common words).

    Use this tool whenever you need objective, exact counts about a
    piece of text rather than estimating them yourself.

    Args:
        text: The text to analyze.

    Returns:
        A string summary of the statistics.
    """
    words = re.findall(r"\b[a-zA-Z']+\b", text)
    word_count = len(words)
    char_count = len(text)
    sentence_count = len(re.findall(r"[.!?]+", text)) or 1

    stopwords = {
        "the", "a", "an", "and", "or", "but", "is", "are", "was", "were",
        "to", "of", "in", "on", "for", "with", "that", "this", "it", "as",
        "be", "by", "at", "from", "we", "you", "i", "he", "she", "they",
    }
    freq = {}
    for w in words:
        wl = w.lower()
        if wl in stopwords or len(wl) <= 2:
            continue
        freq[wl] = freq.get(wl, 0) + 1
    top_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:5]
    top_words_str = ", ".join(f"{w} ({c})" for w, c in top_words) or "none"

    return (
        f"Word count: {word_count}\n"
        f"Character count: {char_count}\n"
        f"Sentence count: {sentence_count}\n"
        f"Top frequent words: {top_words_str}"
    )
