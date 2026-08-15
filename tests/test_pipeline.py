import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).parent.parent))

from src.ocr import extract_text
from src.question_answer import answer_question
from src.summarizer import summarize_text
from src.text_to_speech import generate_speech

import os

# Get absolute paths
project_root = Path(__file__).parent.parent
image_path = project_root / "data" / "input" / "image.png"
output_dir = project_root / "data" / "output"
audio_path = output_dir / "answer.mp3"


#1. ocr 
text = extract_text(image_path)
print(f"\n====Extracted Text===")
print(text)

# 2.summarization 
summary = summarize_text(text)
print(f"\n====Summary====")
print(summary)

#3. Ask a question 

question = input("\n Ask a question about the text: \n")
answer = answer_question(context=text,question=question)

print("\n====Answer====")
print(f"Question: {question}")
print(answer)
print(f"Answer: {answer if answer else 'No answer generated'}")


# 4.text to speech 
print(f"====Generating Speech====")
if answer and answer.strip():
    generate_speech(
        answer,
        str(audio_path)
    )
    
