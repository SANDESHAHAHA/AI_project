#streamlit application
from pathlib import Path
import sys 
import streamlit as st
import os

sys.path.insert(0,str(Path(__file__).parent))

from src.ocr import extract_text
from src.question_answer import answer_question
from src.summarizer import summarize_text
from src.text_to_speech import generate_speech

st.title("Ai learning assistant")

st.write("Upload a study image and let AI extract, ""summarize ,asnwer questions and generate audio.")

uploaded_file = st.file_uploader(
    "Upload an image of your study material",type=["png","jpg","jpeg"]
)

if uploaded_file is not None:
    #saved uploaded image
    image_path = "data/input/uploaded_image.png"
    
    with open(image_path,"wb") as f:
        f.write(uploaded_file.getbuffer())
        
    st.image(
        uploaded_file,
        caption="Uploaded study material")
    
# OCR
if st.button("Extract Text"):

    with st.spinner("Extracting text..."):
        text = extract_text(image_path=image_path)

    st.session_state["text"] = text


if "text" in st.session_state:

    st.subheader("Extracted Text")
    st.write(st.session_state["text"])
    
# summary 
if "text" in st.session_state:
    if st.button("Generate summary"):
        with st.spinner("Generating summary"):
            summary = summarize_text(st.session_state["text"])

        st.session_state["summary"] = summary
if "summary"  in st.session_state:
    st.subheader("Summary")
    st.write(st.session_state["summary"])
        
        
# question answer 

if "text" in st.session_state:
    st.header("Ask a question")
    with st.form("question form"):
        question = st.text_input("Ask a question about your study material:")

        submitted = st.form_submit_button("Get Answer")

        if submitted and question.strip():
            with st.spinner("Finding answer..."):
                answer = answer_question(question=question,context=st.session_state["text"])
    
            st.session_state["answer"] = answer
            st.session_state["question"] = question
    
if "answer" in st.session_state:
    st.subheader("Answer")
    st.write(st.session_state["answer"])
    
if "answer" in st.session_state:
    if st.button("Convert Answer to audio"):
        audio_path = "data/output/answer.mp3"

        generate_speech(
            st.session_state["answer"],
            audio_path
        )
        
        st.audio(audio_path)