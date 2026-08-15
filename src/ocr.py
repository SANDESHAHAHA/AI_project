import os
from pathlib import Path

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import easyocr



reader = easyocr.Reader(["en"])

def extract_text(image_path: str | Path) -> str:
    results = reader.readtext(str(image_path))

    text = " ".join(
        detection[1] for detection in results
    )

    return text

if __name__ == "__main__":
    text= extract_text("../data/input/image.png")
    
    print("\n Extracted Text:")
    print(text)