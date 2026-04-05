
from googletrans import Translator

def translated_text(text:str, from_lang = "en", to_lang = "vi") -> str: 
    translator = Translator()
    result = ""
    try: 
        if not text.strip(): #check vb rỗng hay có khoảng trắng không 
            return ""
        
        #transalate limit 500chars => split size txt, chia nhỏ để dịch hay hơn
        chunk_size = 500
        chunks = [text[i:i+chunk_size] for i in range(0,len(text),chunk_size)]
        for i in chunks:
            translation = translator.translate(i, src = from_lang, dest = to_lang)
            result += translation.text + "\n"
        return result
    except Exception as e:  
        return f"Error {e}"
        