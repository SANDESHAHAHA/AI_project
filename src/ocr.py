import os
from pathlib import Path
from spellchecker import SpellChecker

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import easyocr



reader = easyocr.Reader(["en"])
spell = SpellChecker() #fallback

def extract_text(image_path: str | Path) -> str:
    results = reader.readtext(str(image_path),
            text_threshold=0.5,
            low_text=0.3,
            link_threshold=0.3,
            mag_ratio=1.5)
    for result in results:
        bbox,text,confidence = result
        
    text = " ".join(
        detection[1] for detection in results
    )

    return text

def fallback_correct(text:str)->str:
    words = text.split()
    corrected_words =[]
    
    for word in words:
        stripped = word.strip(".,!?:;()[]\"'")
        prefix = word[:len(word) - len(word.lstrip(".,!?:;()[]\"'"))]
        suffix = word[len(stripped)+len(prefix):]
        
        if not stripped or not stripped.isalpha():
            corrected_words.append(word)
            continue
        
        # skip correction if already a known word (case-insensitive)
        if stripped.lower() in spell:
            corrected_words.append(word)
            continue
        
        correction = spell.correction(stripped)
        if correction and correction.lower() != stripped.lower():
            # preserve original capitalization styoe 
            if stripped.isupper():
                correction = correction.upper()
            elif stripped[0].isupper():
                correction = correction.capitalize()
            corrected_words.append(prefix+correction+suffix)
        else:
            corrected_words.append(word)
            
    return " ".join(corrected_words)

if __name__ == "__main__":
    text= extract_text("../data/input/image.png")
    corrected_text = fallback_correct(text)
    print("\n Extracted Text:")
    print(corrected_text)