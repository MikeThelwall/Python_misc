# -*- coding: utf-8 -*-
"""
Created on Tue Jul 9 05:44:02 2024
Convert academic PDF to text, keeping paragraphs as far as possible, excluding figures.
#PyPDF2 introduces errors by merging lines DO NOT USE
#Fitz/PyMuPDF ignores figures and paragrpahs, listing text as it is.
@author: Mike Thelwall
"""
import fitz #pip3 install PyMuPDF
import os, sys

pdf_directories = ["C:/Users/Mike Thelwall/pdf/","C:/Users/Mike Thelwall/pdf/second set/"]

def convert_pdf_to_text_by_paragraphs_fitz(pdf_file, output_file):
  """
  Processes a PDF file, with double newline between paragraphs.
  """
  text = ""
  page_no = 0
  doc = fitz.open(pdf_file)
  for page in doc:
   page_no += 1
   text += "$$$pageE No:" + str(page_no) + "\n\n"
   blocks = page.get_text("blocks")
   for block in blocks:
        if block[4]:
          text += block[4].strip() + "\n\n" #removes any leading, and trailing whitespaces.
  doc.close()
  with open(output_file + "_fitz_blocks_pages.text", 'w', encoding='utf-8') as f:
    f.write(text)

def convert_pdfs_to_text_by_paragraphs_fitz(pdf_directory):
    directory = os.fsencode(pdf_directory)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".pdf"): 
            print(filename)
            pdf_file = pdf_directory + filename
            convert_pdf_to_text_by_paragraphs_fitz(pdf_file, pdf_file)

for pdf_directory in pdf_directories:
    print(pdf_directory)
    convert_pdfs_to_text_by_paragraphs_fitz(pdf_directory)
print("Now process with Webometric Analyst Services/pdf menu")