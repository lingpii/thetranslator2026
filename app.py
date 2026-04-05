import streamlit as st
import os
from pdf_reader import read_pdf
from translation import translated_text
from audio_converter import audio_converted

def local_css(file_name):
    """Hàm đọc file CSS từ thư mục cục bộ"""
    if os.path.exists(file_name):
        with open(file_name, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main(): 
    # 1. THIẾT LẬP GIAO DIỆN & TITLE TRONG CSS
    # Gọi file CSS thay vì viết trực tiếp
    local_css("style.css")

    # Hiển thị Title với Style đã định nghĩa

    
    st.markdown('<div class="pixel-divider" style="text-align: center;>𓇼 ⋆.˚ 𓆉 𓆝 𓆡⋆.˚ 𓇼</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">✦ The Translator ✦</h1>', unsafe_allow_html=True)
    st.markdown('<div class="pixel-divider">──────────────────── ⋆⋅𖤓⋅⋆ ────────────────────</div>', unsafe_allow_html=True)
    
    #Chia layout: 
    col1, col2 = st.columns(2,gap="large")

    #Trạng thái session_state, trạng thái nút bấm 
    if "clicked" not in st.session_state:
        st.session_state.clicked = False

    #PHẦN CODE CHÍNH 

    #Step 1: input (text or pdf)
    # Trong hàm main(), thay thế đoạn code chọn input cũ:
    with col1: 
        st.markdown("### 📝 Bản gốc")
        
        # Sử dụng Tabs để tạo hiệu ứng nút bấm qua lại
        tab1, tab2 = st.tabs(["⌨️ Nhập text", "📁 Upload PDF"])
        
        with tab1:
            text_input = st.text_area("Văn bản...", height=250, key="text_input")
        
        with tab2:
            file = st.file_uploader("Tải lên PDF", type="pdf", key="file_input")
            pdf_text = ""
            if file is not None:
                pdf_text = read_pdf(file)
                st.success("Đã đọc PDF!")
    
        # Xác định nội dung text dựa trên tab đang hoạt động (ưu tiên PDF nếu có file)
        text = pdf_text if file else text_input
    
        if st.button("Translate it!", type="secondary", use_container_width=True):
            st.session_state.clicked = True
        # Sau đó dùng chung 1 hàm dịch
        #Step 2: Translate it 
        with col2:
            st.markdown("### Bản dịch của bạn: ")
            if st.session_state.clicked and text.strip(): #Check input 
                with st.spinner ("Đang dịch!"): 
                    result = translated_text(text)  # từ translator.py
                    st.info(result) #show output 
                    #Step 3: output and convert to audio 
                    audio_path = audio_converted(result)
                    if audio_path: 
                        st.success("Done!")
                        st.audio(audio_path)
                        st.session_state.clicked = False #reset
            else: st.write("✿✿✿")
        
        if st.session_state.clicked and not text.strip(): 
            st.warning(" Bạn chưa nhập nội dung -_- !")
            st.session_state.clicked = False #reset

if __name__ == "__main__": 
    main()
