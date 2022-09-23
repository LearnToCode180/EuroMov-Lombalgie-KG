import pdfplumber
import sys

import fitz
from os import mkdir, listdir
from os.path import isfile, join

import re
import pytesseract


pdf_file = sys.argv[1]
save_path = sys.argv[2]

#--------------------------------------------Extraction du texte--------------------------------------------#

text_pages = []
with pdfplumber.open(pdf_file) as pdf:
    for page in pdf.pages:
        text_pages.append(page.extract_text())
        
pdf_file_fitz = fitz.open(pdf_file)


#--------------------------------------------Extraction d'images--------------------------------------------#

images_path = join(save_path, 'images')
mkdir(images_path)

for page_index in range(len(pdf_file_fitz)):
    
    # get the page itself
    page = pdf_file_fitz[page_index]
    image_list = page.getImageList()
      
    # printing number of images found in this page
    if image_list:
        print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
        for image_index, img in enumerate(page.getImageList(), start=1):
        
            # get the XREF of the image
            xref = img[0]
            pix = fitz.Pixmap(pdf_file_fitz, xref)
            if pix.n < 5:       # this is GRAY or RGB
                pix.save(join(images_path, "page_%s.png" % (page_index)))
            else:               # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix1.save(join(images_path, "page_%s.png" % (page_index)))
                pix1 = None
            pix = None
        
    else:
        print("[!] No images found on page", page_index)

#--------------------------------------------Extraction du texte des images--------------------------------------------#        

num = re.compile(r'\d+')

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

images = [f for f in listdir(images_path) if isfile(join(images_path, f))]

for img in images:
    numPage = num.findall(img)[0]
    # print(numPage)
    text_extracted = pytesseract.image_to_string(join(images_path, img))
    # print(text_extracted)
    text_pages.insert(int(numPage) + 1, text_extracted)

#--------------------------------------------Enregistrement du texte extrait--------------------------------------------#

allText = ''.join(text_pages)

with open(join(save_path, 'allText.txt'), 'w', encoding="utf-8") as f:
    f.write(allText)

print("Extraction Reussie !!")    

# python TextExtraction.py rapport_lombalgie.pdf C:\Users\Anas\Desktop\M2SI\S4 C:\Users\Anas\Desktop