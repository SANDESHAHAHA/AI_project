# text to audio

from gtts import gTTS 

def generate_speech(text:str,output_file:str)->None:
    
    if not text.strip():
        return 
    
    tts = gTTS(text=text,lang="en")
    tts.save(output_file)
    
    
if __name__ == "__main__":
    
    text = """
    Photosynthesis is the process by which green plants convert light energy into chemical energy .
    """
    
    output_file = "../data/output/answer.mp3"
    generate_speech(text,output_file=output_file)
    print(f"Audio saved to : {output_file}")