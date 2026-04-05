import asyncio
import edge_tts 

def audio_converted (text, lang = "vi"): 
    output_file = "record.mp3"
    voice = "vi-VN-HoaiMyNeural"
    async def run_tts(): 
        communicate = edge_tts.Communicate(text,voice) # tạo đối tượng để link với Microsoft
        await communicate.save(output_file)
    try: 
        if text.strip(): 
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(run_tts())
            loop.close()
        else: 
            return None
    except Exception as e: 
        print(f"Error: {e}")
        return None
    return output_file
    