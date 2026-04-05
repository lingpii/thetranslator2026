
from pypdf import PdfReader
#limit characters for input
MAX_CHARS = 3000
def read_pdf(uploaded_file) -> str: 
    #Read file pdf from upload: 
    reader = PdfReader(uploaded_file)

    #Pages: 

    num_page = len(reader.pages)

    #Read pages context 
    pages_txt = ""
    for i in range(num_page):
        page = reader.pages[i]
        pages_txt += page.extract_text()
        if pages_txt: 
            pages_txt += pages_txt + "\n"
    
    # if input len > max_chars => only read to the amount of max_chars
    if len(pages_txt) > MAX_CHARS: 
        pages_txt = pages_txt[:MAX_CHARS]
    
    return pages_txt
