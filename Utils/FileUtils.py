from docx2pdf import convert
from pdf2image import convert_from_path
from PIL import ImageFile, Image
import os

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

input_directory = "C:\\Users\\kaiboey2\\Downloads\\PhDQE-2020-Q3A\\"
#input_directory = "C:\\Users\\kaiboey2\\Documents\\input_directory\\"
output_directory = "C:/Users/kaiboey2/Documents/tempfiles2/"

def genoutputfiles():
    dirs = os.listdir(input_directory)

    for file in dirs:
        file_name, extension = os.path.splitext(file)
        if 'pdf' in extension:
            pdf2png(input_directory,file_name)
        elif 'docx' in extension or 'doc' in extension:
            docx2pdf(input_directory,file_name,extension)

#poppler_path required for windows
def pdf2png(directory,pdf_name):
    try:
        pages = convert_from_path(os.path.join(directory, pdf_name+'.pdf'), dpi=600, poppler_path = r"C:\Users\kaiboey2\Downloads\Release-21.10.0-0\poppler-21.10.0\Library\bin")
        for idx, page in enumerate(pages):
            page.save(os.path.join(output_directory, pdf_name) + "_{}.png".format(idx), 'PNG')
    except IndexError as e:
        print(e)



def docx2pdf(directory,docx_name,extension):
    try:
        output_file_name = "{}.pdf".format(docx_name)
        input_file = os.path.join(directory, docx_name+extension)
        output_file = os.path.join(directory, output_file_name)
        convert(input_file, output_file)
        pdf2png(directory, docx_name)
        os.remove(output_file)
    except IndexError as e:
        print(e)

# def pdf2png(directory,pdf_name):
#     try:
#         doc = fitz.open(directory+pdf_name+'.pdf')
#         page_count = len(doc)
#         for idx in range(page_count):
#             page = doc.loadPage(idx)  # number of page
#             pix = page.getPixmap()
#             pix.set_dpi()
#             output = os.path.join(output_directory, pdf_name) + "_{}.png".format(idx)
#             print("write to path: {}".format(output))
#             pix.writePNG(output)
#     except:
#         print("convert to png exception")