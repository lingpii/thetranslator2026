import re

from deep_translator import GoogleTranslator


MAX_CHUNK_SIZE = 1800


def _split_large_paragraph(paragraph: str, chunk_size: int = MAX_CHUNK_SIZE) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", paragraph)
    chunks: list[str] = []
    current = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        candidate = f"{current} {sentence}".strip()
        if current and len(candidate) > chunk_size:
            chunks.append(current)
            current = sentence
        elif len(sentence) > chunk_size:
            if current:
                chunks.append(current)
                current = ""
            for start in range(0, len(sentence), chunk_size):
                chunks.append(sentence[start:start + chunk_size])
        else:
            current = candidate

    if current:
        chunks.append(current)

    return chunks or [paragraph[:chunk_size]]


def _translate_paragraph(paragraph: str, translator: GoogleTranslator) -> str:
    cleaned = paragraph.strip()
    if not cleaned:
        return ""

    if len(cleaned) <= MAX_CHUNK_SIZE:
        return translator.translate(cleaned)

    parts = _split_large_paragraph(cleaned)
    translated_parts = [translator.translate(part) for part in parts if part.strip()]
    return " ".join(part.strip() for part in translated_parts if part and part.strip())


def translated_text(text: str, from_lang: str = "auto", to_lang: str = "vi") -> str:
    cleaned_text = (text or "").strip()
    if not cleaned_text:
        return ""

    try:
        translator = GoogleTranslator(source=from_lang, target=to_lang)
        paragraphs = re.split(r"\n\s*\n", cleaned_text)
        translated_paragraphs = [
            _translate_paragraph(paragraph, translator)
            for paragraph in paragraphs
            if paragraph.strip()
        ]
        return "\n\n".join(paragraph for paragraph in translated_paragraphs if paragraph)
    except Exception as exc:
        return f"Error: {exc}"
