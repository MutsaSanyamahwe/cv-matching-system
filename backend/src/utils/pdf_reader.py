"""
PDF Reader utility functions
This is a pipline to read the PDF files and extract the text from them.
 It uses the PyPDF2 library to read the PDF files and extract the text from them. 
 This pipeline is for user uploads and is not used in the main pipeline to convert the PDF files in the dataset to text files.
 It is lightweight and there is no need to save the extracted text to a txt file. The extracted text is returned as a string.
"""

import PyPDF2

def extract_text_from_pdf(file):
    """
    Extract text from uploaded PDF file
    """
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text
