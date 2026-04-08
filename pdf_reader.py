from pypdf import PdfReader


MAX_CHARS = 6000


def read_pdf(uploaded_file) -> str:
    reader = PdfReader(uploaded_file)
    pages_text: list[str] = []

    for page in reader.pages:
        page_text = (page.extract_text() or "").strip()
        if page_text:
            pages_text.append(page_text)

    combined_text = "\n\n".join(pages_text)
    return combined_text[:MAX_CHARS]
