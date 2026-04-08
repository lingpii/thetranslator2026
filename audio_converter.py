import asyncio
import re

import edge_tts


VOICE_MAP = {
    "vi": "vi-VN-HoaiMyNeural",
    "en": "en-US-JennyNeural",
}

MAX_TTS_CHARS = 2500


def _split_tts_text(text: str, chunk_size: int = MAX_TTS_CHARS) -> list[str]:
    normalized_text = re.sub(r"\s+", " ", (text or "").strip())
    if not normalized_text:
        return []

    sentences = re.split(r"(?<=[.!?])\s+", normalized_text)
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

    return chunks


def audio_converted(text: str, lang: str = "vi") -> tuple[bytes | None, str | None]:
    chunks = _split_tts_text(text)
    if not chunks:
        return None, "Không có nội dung để tạo audio."

    voice = VOICE_MAP.get(lang, VOICE_MAP["vi"])

    async def run_tts() -> bytes:
        audio_bytes = bytearray()
        for chunk in chunks:
            communicate = edge_tts.Communicate(chunk, voice)
            async for item in communicate.stream():
                if item["type"] == "audio":
                    audio_bytes.extend(item["data"])
        return bytes(audio_bytes)

    try:
        audio_bytes = asyncio.run(run_tts())
        if not audio_bytes:
            return None, "Dịch vụ tạo giọng nói không trả về dữ liệu audio."
        return audio_bytes, None
    except Exception as exc:
        return None, f"Lỗi audio: {exc}"
