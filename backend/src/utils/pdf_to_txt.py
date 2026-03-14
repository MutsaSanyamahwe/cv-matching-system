# Code in this file is for converting the text in the PDF's and saving it in txt files
from pathlib import Path
import PyPDF2

#Root folder with the folder with job categories
resume_root = Path("data/resumes")

#Path to store the text files
txt_root = Path("data/resumes_txt")
txt_root.mkdir(exist_ok=True)  # Create the directory if it doesn't exist

#Looping through each category
for job_folder in resume_root.iterdir():
    if job_folder.is_dir():
        print(f"\nProcessing category: {job_folder.name}")

        #Create corresponding folder in resumes_txt
        job_txt_folder = txt_root/job_folder.name
        job_txt_folder.mkdir(exist_ok=True)

        #Looping through each resume in the category
        for pdf_file in job_folder.glob("*.pdf"):
            print(f"Processing file: {pdf_file.name}")
            
            #open pdf and extracting text
            with open(pdf_file, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"

                #Saving the extracted text to a txt file
                txt_file = job_txt_folder / (pdf_file.stem + ".txt")
                with open(txt_file, "w", encoding="utf-8") as txt:
                    txt.write(text) 
            print(f"Saved text to: {txt_file}")
print("\nAll files processed and saved in txt format.")







                      

