from collections import Counter

from underthesea import classify, sentiment, word_tokenize


STOPWORDS = {
    "anh", "ấy", "bên", "bởi", "các", "cần", "chỉ", "cho", "có", "của",
    "cùng", "đã", "đang", "đây", "để", "đến", "được", "hay", "hơn", "khi",
    "không", "làm", "là", "một", "nếu", "ngày", "người", "nhiều", "những",
    "ở", "sau", "sẽ", "số", "tại", "theo", "thì", "trên", "trong", "từ",
    "vào", "vẫn", "và", "với",
}

TOPIC_FALLBACKS = {
    "Công nghệ": {"công nghệ", "ai", "dữ liệu", "phần mềm", "hệ thống", "ứng dụng"},
    "Kinh doanh": {"doanh nghiệp", "công ty", "khách hàng", "thị trường", "sản phẩm", "doanh thu"},
    "Tài chính": {"tài chính", "ngân hàng", "đầu tư", "lợi nhuận", "chi phí", "tài sản"},
    "Giáo dục": {"giáo dục", "trường", "sinh viên", "học sinh", "đào tạo", "chương trình"},
    "Sức khỏe": {"sức khỏe", "y tế", "bệnh viện", "bác sĩ", "điều trị", "bệnh nhân"},
    "Pháp luật": {"pháp luật", "quy định", "hợp đồng", "tranh chấp", "pháp lý", "điều khoản"},
}

CLASSIFY_TOPIC_MAP = {
    "K": "Kinh doanh",
    "Công nghệ": "Công nghệ",
    "Kinh doanh": "Kinh doanh",
    "Tài chính": "Tài chính",
    "Giáo dục": "Giáo dục",
    "Sức khỏe": "Sức khỏe",
    "Pháp luật": "Pháp luật",
}

TOPIC_SUMMARIES = {
    "Công nghệ": "Nội dung tập trung vào hệ thống, phần mềm, dữ liệu hoặc ứng dụng công nghệ.",
    "Kinh doanh": "Nội dung xoay quanh doanh nghiệp, khách hàng, sản phẩm hoặc tăng trưởng thị trường.",
    "Tài chính": "Nội dung nghiêng về ngân sách, đầu tư, dòng tiền hoặc hiệu quả tài chính.",
    "Giáo dục": "Nội dung nói về học tập, đào tạo, nghiên cứu hoặc môi trường giảng dạy.",
    "Sức khỏe": "Nội dung liên quan đến y tế, điều trị, chăm sóc sức khỏe hoặc bệnh lý.",
    "Pháp luật": "Nội dung có yếu tố quy định, hợp đồng, nghĩa vụ hoặc xử lý pháp lý.",
    "Chưa phân loại": "Chưa xác định rõ chủ đề nổi bật, có thể cần thêm ngữ cảnh hoặc văn bản dài hơn.",
}

SENTIMENT_LABELS = {
    "positive": ("Tích cực", "Nội dung nghiêng về kết quả tốt, cơ hội hoặc tín hiệu lạc quan."),
    "negative": ("Tiêu cực", "Nội dung nhấn mạnh rủi ro, vấn đề hoặc chiều hướng bất lợi."),
    "neutral": ("Trung tính", "Nội dung thiên về truyền đạt thông tin, chưa bộc lộ cảm xúc mạnh."),
}


def _tokenize(text: str) -> list[str]:
    try:
        return word_tokenize(text)
    except Exception:
        return text.split()


def _clean_tokens(text: str) -> list[str]:
    tokens = _tokenize(text)
    cleaned_tokens = []
    for token in tokens:
        normalized = token.strip().lower()
        if len(normalized) < 2 or normalized in STOPWORDS:
            continue
        cleaned_tokens.append(normalized)
    return cleaned_tokens


def get_sentiment(text: str) -> str:
    try:
        return sentiment(text)
    except Exception:
        return "neutral"


def _fallback_topic(text: str) -> tuple[str, str]:
    token_set = set(_clean_tokens(text))
    best_topic = "Chưa phân loại"
    best_score = 0

    for topic, keywords in TOPIC_FALLBACKS.items():
        score = len(token_set & keywords)
        if score > best_score:
            best_score = score
            best_topic = topic

    if best_score >= 2:
        return best_topic, "Vừa"
    if best_score == 1:
        return best_topic, "Thấp"
    return "Chưa phân loại", "Thấp"


def get_topic(text: str) -> tuple[str, str]:
    try:
        result = classify(text)
        if result:
            raw_topic = str(result[0]).strip()
            mapped_topic = CLASSIFY_TOPIC_MAP.get(raw_topic, raw_topic)
            if mapped_topic and len(mapped_topic) >= 3:
                return mapped_topic, "Cao"
    except Exception:
        pass

    return _fallback_topic(text)


def get_keywords(text: str, top_n: int = 8) -> list[str]:
    try:
        cleaned_tokens = _clean_tokens(text)
        counts = Counter(cleaned_tokens)
        ranked = counts.most_common(top_n * 3)

        keywords: list[str] = []
        seen_single_terms: set[str] = set()

        for word, _ in ranked:
            parts = word.split()
            if len(parts) == 1 and len(word) < 4:
                continue
            if len(parts) > 1:
                if any(part in seen_single_terms for part in parts):
                    continue
                seen_single_terms.update(parts)
            else:
                if word in seen_single_terms:
                    continue
                seen_single_terms.add(word)

            keywords.append(word)
            if len(keywords) >= top_n:
                break

        return keywords
    except Exception:
        return []


def build_analysis(text: str) -> dict[str, object]:
    topic, confidence = get_topic(text)
    sentiment_code = get_sentiment(text)
    keywords = get_keywords(text)

    sentiment_title, sentiment_description = SENTIMENT_LABELS.get(
        sentiment_code,
        SENTIMENT_LABELS["neutral"],
    )

    normalized_topic = topic if topic else "Chưa phân loại"
    topic_summary = TOPIC_SUMMARIES.get(normalized_topic, "Nội dung thuộc một nhóm chủ đề tổng quát được mô hình nhận diện.")

    return {
        "topic": normalized_topic,
        "topic_summary": topic_summary,
        "topic_confidence": confidence,
        "sentiment": sentiment_title,
        "sentiment_summary": sentiment_description,
        "keywords": keywords,
        "keyword_summary": " | ".join(keywords[:4]) if keywords else "Không tìm thấy từ khóa nổi bật",
    }
