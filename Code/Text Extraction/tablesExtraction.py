import camelot
import sys
from os.path import join
from os import mkdir
import time

pdf_file = sys.argv[1]
save_path = sys.argv[3]

#--------------------------------------------Extraction des tableaux--------------------------------------------#

tables = camelot.read_pdf(pdf_file, pages='all')
print("Total tables extracted: ", tables.n)

#--------------------------------------------Enregistrement des tableaux extraits--------------------------------------------#

tableaux_path = join(save_path, 'tableaux')
mkdir(tableaux_path)

animation = "|/-\\"

i = 0
for i in range(tables.n):
    tables[i].to_excel(join(tableaux_path, f'tableau{i}.xlsx'), encoding='utf-8')
    sys.stdout.write("\r" + animation[i % len(animation)])
    sys.stdout.flush()
    
# python tablesExtraction.py rapport_lombalgie.pdf C:\Users\Anas\Desktop\M2SI\S4 C:\Users\Anas\Desktop