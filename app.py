from pathlib import Path

import streamlit as st

from audio_converter import audio_converted
from pdf_reader import read_pdf
from summarize import summarize
from text_analyzer import get_keywords, get_sentiment, get_topic
from translation import translated_text


BASE_DIR = Path(__file__).resolve().parent


def local_css(file_name: str) -> None:
    css_path = BASE_DIR / file_name
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def build_source_text(text_input: str, uploaded_file) -> str:
    if uploaded_file is not None:
        return read_pdf(uploaded_file)
    return (text_input or "").strip()


def normalize_sentences(text: str) -> list[str]:
    return [sentence.strip(" -\n") for sentence in text.splitlines() if sentence.strip()]


def render_audio(text: str, lang: str = "vi") -> None:
    st.markdown("### Audio")
    audio_bytes, audio_error = audio_converted(text, lang=lang)
    if audio_bytes:
        st.audio(audio_bytes, format="audio/mp3")
        st.download_button(
            "Tải audio xuống",
            data=audio_bytes,
            file_name="translator-audio.mp3",
            mime="audio/mpeg",
            use_container_width=True,
        )
    else:
        st.warning(audio_error or "Không tạo được audio lúc này. Bạn vẫn có thể xem nội dung văn bản ở trên.")


def render_analysis(sentiment_val: str, topic: str, keywords: list[str]) -> None:
    if sentiment_val == "positive":
        sentiment_label = "Tích cực"
    elif sentiment_val == "negative":
        sentiment_label = "Tiêu cực"
    else:
        sentiment_label = "Trung tính"

    topic_label = "Chưa phân loại" if topic == "unknown" else str(topic).capitalize()
    keyword_label = ", ".join(keywords) if keywords else "Không tìm thấy"

    st.markdown(
        f"""
        <div class="analysis-grid">
            <div class="analysis-card">
                <div class="analysis-title">Chủ đề</div>
                <div class="analysis-value">{topic_label}</div>
            </div>
            <div class="analysis-card">
                <div class="analysis-title">Cảm xúc</div>
                <div class="analysis-value">{sentiment_label}</div>
            </div>
            <div class="analysis-card analysis-card-wide">
                <div class="analysis-title">Từ khóa nổi bật</div>
                <div class="analysis-value">{keyword_label}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_translate_result(text: str) -> None:
    st.markdown("### Bản dịch của bạn")
    with st.spinner("Đang dịch..."):
        result = translated_text(text)

    if result.startswith("Error:"):
        st.error(result)
        return

    st.text(result)
    render_audio(result, lang="vi")


def render_summary_result(text: str) -> None:
    st.markdown("### Kết quả tóm tắt và phân tích")
    with st.spinner("Đang xử lý tóm tắt và phân tích..."):
        english_source = translated_text(text, from_lang="auto", to_lang="en")
        if english_source.startswith("Error:"):
            st.error(english_source)
            return

        english_points = summarize(english_source)
        if not english_points:
            english_points = summarize(text)

        english_summary = "\n".join(f"- {sentence}" for sentence in english_points)
        vietnamese_summary = translated_text(english_summary, from_lang="auto", to_lang="vi")

    if vietnamese_summary.startswith("Error:"):
        st.error(vietnamese_summary)
        return

    vietnamese_points = normalize_sentences(vietnamese_summary.replace("- ", ""))
    if not vietnamese_points:
        vietnamese_points = normalize_sentences(vietnamese_summary)

    topic = get_topic(vietnamese_summary)
    sentiment_val = get_sentiment(vietnamese_summary)
    keywords = get_keywords(vietnamese_summary)

    english_html = "".join(f"<li>{sentence}</li>" for sentence in english_points)
    vietnamese_html = "".join(f"<li>{sentence}</li>" for sentence in vietnamese_points)

    st.markdown(
        f"""
        <div class="summary-box">
            <div class="summary-section">
                <div class="summary-header">Key Points (English)</div>
                <ul>{english_html}</ul>
            </div>
            <div class="summary-section">
                <div class="summary-header">Tóm tắt (Tiếng Việt)</div>
                <ul>{vietnamese_html}</ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_analysis(sentiment_val, topic, keywords)
    render_audio(vietnamese_summary, lang="vi")


def main() -> None:
    st.set_page_config(page_title="The Translator", page_icon=":scroll:", layout="wide")
    local_css("style.css")

    st.markdown('<div class="hero-shell">', unsafe_allow_html=True)
    st.markdown('<div class="pixel-divider">THE TRANSLATOR</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">Translate, summarize, and listen in one flow</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-subtitle">Paste text or upload a PDF, then turn it into a cleaner Vietnamese output with optional audio.</p>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.05, 1], gap="large")

    with col1:
        st.markdown("### Nguồn nội dung")
        tab1, tab2 = st.tabs(["Nhập văn bản", "Upload PDF"])

        pdf_text = ""
        uploaded_file = None

        with tab1:
            text_input = st.text_area(
                "Văn bản đầu vào",
                height=280,
                placeholder="Dán nội dung cần dịch hoặc tóm tắt tại đây...",
            )

        with tab2:
            uploaded_file = st.file_uploader("Chọn file PDF", type="pdf")
            if uploaded_file is not None:
                pdf_text = read_pdf(uploaded_file)
                if pdf_text:
                    st.success("PDF đã được đọc thành công.")
                else:
                    st.warning("Không tìm thấy nội dung văn bản trong file PDF này.")

        source_text = build_source_text(text_input, uploaded_file)
        char_count = len(source_text)
        st.caption(f"Số ký tự đang xử lý: {char_count}")

        translate_col, summarize_col = st.columns(2)
        run_translate = translate_col.button("Translate it!", use_container_width=True)
        run_summary = summarize_col.button("Summarize it!", type="primary", use_container_width=True)

    with col2:
        st.markdown("### Kết quả")
        if run_translate:
            if source_text.strip():
                render_translate_result(source_text)
            else:
                st.warning("Bạn chưa nhập nội dung để dịch.")
        elif run_summary:
            if source_text.strip():
                render_summary_result(source_text)
            else:
                st.warning("Bạn chưa nhập nội dung để tóm tắt.")
        else:
            st.markdown(
                """
                <div class="empty-state">
                    <div class="empty-title">Sẵn sàng xử lý</div>
                    <p>Chọn một thao tác ở bên trái để xem bản dịch, bản tóm tắt và audio ở đây.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    main()
