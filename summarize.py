import re
from newspaper import Article


def _split_sentences(text: str) -> list[str]:
    """Tách summary thành câu — cherry-pick từ codex"""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def summarize(text: str, num_sentences: int = 5) -> list[str]:
    try:
        # newspaper3k — đúng bài học
        article = Article(url='')
        article.set_text(text)
        article.nlp()
        summary = article.summary

        if not summary:
            return _split_sentences(text)[:num_sentences]

        sentences = _split_sentences(summary)
        return sentences[:num_sentences]

    except Exception:
        # Fallback đơn giản
        return _split_sentences(text)[:num_sentences]