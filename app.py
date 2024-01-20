import streamlit as st
import PyPDF2 as pdf
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input: str) -> dict:
    """
    This function uses the Google Generative AI API to generate text using the Gemini model.

    Args:
        input (str): The text input to be used for generation.

    Returns:
        dict: A JSON response from the API containing the generated text.

    """
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input)
    return response.text


def input_pdf_text(uploaded_file: bytes) -> str:
    """
    This function takes a PDF file as input and returns the text content of the PDF.

    Args:
        uploaded_file (bytes): The PDF file as a byte string.

    Returns:
        str: The text content of the PDF file.

    """
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text


# Prompt Template

input_prompt = """
Hey act like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of tech field , software engineering , data science,
data analysis and big data engineer. Your task is to evaluate the 
resume based on the given job description. You must consided the job market is
very competitive and you must provide best assistance for improving the
resumes. Assign the percentage matching based on the jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure 
{{"JD Match":"%",MissingKeywords":"[]","Profile Summary":""}}
"""

# Streamlit App

st.title("Smart Application Tracking System")
st.text("Improve Your Resume with ATS")
jd = st.text_area("Past the job description")
uploaded_file = st.file_uploader(
    "Upload your resume", type="pdf", help="Please upload the PDF")
submit = st.button("Submit")


if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt)
        st.subheader(response)
