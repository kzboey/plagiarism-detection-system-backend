from utils.fileutils import Files
import sys, getopt
from utils.uuidgenerator import gen_uuid4,gen_randomid
from cryptography.fernet import Fernet
import os
import numpy as np
import base64
from PIL import Image
from utils.imageutils import convert_base64
import time
from pdf2image import convert_from_path
import PyPDF2
from PyPDF2 import PdfFileWriter
from docx2pdf import convert
from utils.fileutils import docx2pdf2


def encodebase64(file):

    image_file = Image.open(file)
    image_file.save("temp.png", optimize=True, quality=10)
    with open("temp.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode("utf-8")

def convert_2_image(fpath,fname):

    file = os.path.join(fpath, fname)
    pdf = PyPDF2.PdfFileReader(file)

    for page in range(pdf.getNumPages()):
        pgnum = page+1
        pdfwrite = PdfFileWriter()
        pdfwrite.addPage(pdf.getPage(page))
        outputfilename = '{}_page_{}.pdf'.format(
            fname, pgnum)
        outputfile = os.path.join('C:/Users/kaiboey2/Documents/test_split_convert', outputfilename)
        with open(outputfile, 'wb') as out:
            pdfwrite.write(out)

        if os.path.isfile(outputfile):
            page = convert_from_path(outputfile, dpi=500,
                                     poppler_path=r"C:\Users\kaiboey2\Downloads\Release-21.10.0-0\poppler-21.10.0\Library\bin")
            page[0].save(os.path.join(fpath, fname) + "_{}.png".format(pgnum), 'PNG')

def docx2pdf(directory,docx_name,extension):

    try:
        output_file_name = "{}.pdf".format(docx_name)
        input_file = os.path.join(directory, docx_name+extension)
        output_file = os.path.join(directory, output_file_name)
        convert(input_file, output_file)
        convert_2_image(directory, output_file_name)
        os.remove(output_file)
    except IndexError as e:
        print(e)
        return False

    return True

def main():
    time_start = time.time()
    fpath = "C:/temp/documents/433910_CS665_testos/panriwei/"
    fname = 'panriwei_89420_8905023_PANRIWEI_55243049_1'
    # convert_2_image(fpath,fname)
    docx2pdf2(fpath,fname,'.docx')
    # base64_str = encodebase64(file)
    # f = open("tempfile3.txt", "w")
    # f.write(base64_str)
    # f.close()
    list = [1,2,3,4,5]
    print(list[0])
    time_end = time.time()
    print("Seconds since epoch =", time_end-time_start)

if __name__ == "__main__":
    main()

