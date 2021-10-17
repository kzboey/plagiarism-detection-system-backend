import fitz
from docx2pdf import convert
import os

input_directory = "C:\\Users\\kaiboey2\\Downloads\\PhDQE-2020-Q3A\\"
output_directory = "C:/Users/kaiboey2/Documents/tempfiles/"

def generateOutputFiles():
    dirs = os.listdir(input_directory)

    for file in dirs:
        file_name, extension = os.path.splitext(file)
        if 'pdf' in extension:
            pdfToPng(input_directory,file_name)
        elif 'docx' in extension or 'doc' in extension:
            docxToPdf(input_directory,file_name,extension)

def pdfToPng(directory,file_name):
    try:
        doc = fitz.open(directory+file_name+'.pdf')
        page_count = len(doc)
        for idx in range(page_count):
            page = doc.loadPage(idx)  # number of page
            pix = page.getPixmap()
            output = os.path.join(output_directory, file_name) + "_{}.png".format(idx)
            print("write to path: {}".format(output))
            pix.writePNG(output)
    except:
        print("convert to png exception")

def docxToPdf(directory,file_name,extension):
    try:
        output_file_name = "{}.pdf".format(file_name)
        input_file = os.path.join(directory, file_name+extension)
        output_file = os.path.join(directory, output_file_name)
        convert(input_file, output_file)
        pdfToPng(directory, file_name)
        os.remove(output_file)
    except:
        print("convert to pdf exception")