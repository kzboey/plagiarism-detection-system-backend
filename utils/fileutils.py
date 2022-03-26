import PyPDF2
from PyPDF2 import PdfFileWriter
from docx2pdf import convert
from pdf2image import convert_from_path
from PIL import ImageFile, Image, ExifTags
from zipfile import ZipFile
import os
from os.path import join, isdir, isfile, exists, splitext
import shutil
from werkzeug.utils import secure_filename
import cv2
import time
from environ import get_env
import threading
from utils.logger import logger

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None


#read from config file in future
# default_input_dir = "C:\\Users\\kaiboey2\\Downloads\\others-midterm\\"
default_input_dir = "C:\\Users\\kaiboey2\\Documents\\orientation_files\\"
default_output_dir = "C:/Users/kaiboey2/Documents/oent_files_output/"
# default_input_dir = "/Users/boeykaizhe/projects/plagiarism-detection-webapp/public"
# default_output_dir = "/Users/boeykaizhe/projects/plagiarism-detection-webapp/temp"

ALLOWED_EXTENSIONS = set(['zip', 'doc', 'docx', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file(file, path):
    try:
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(join(path, filename))
            logger.info("File: {} Uploaded ".format(file.filename))
            return True
        else:
            logger.info("File: {} Upload Fail ".format(file.filename))
            raise Exception("Invalid File Type")
        return False
    except IndexError as e:
        logger.exception(e)
        return False


def make_directory(dir):
    dirName = dir

    try:
        os.makedirs(dirName)
        logger.info("Directory {} Created ".format(dirName))
    except FileExistsError:
        logger.info("Directory {} already exists ".format(dirName))

    return dirName


def get_author(filename):
    author_name = ''
    for element in range(0, len(filename)):
        if filename[element] == '_':
            author_name = filename[:element]
            break
    return author_name

def docx2pdf2(directory,docx_name,extension):
    output_file_name = "{}.pdf".format(docx_name)
    input_file = join(directory, docx_name+extension).replace("\\", "/") # file | Input file to perform the operation on.
    pdf_name = join(directory, output_file_name).replace("\\", "/")
    try:
        convert(input_file, pdf_name)
    except IndexError as e:
        print(e)

class Files:

    def __init__(self, resolution=500, input_directory=default_input_dir, output_directory=default_output_dir):
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.resolution = resolution

    def genoutputfiles(self): #temp_path of extracted zip file

        for file in os.listdir(self.input_directory):
            check_dir_exist = join(self.input_directory, file).replace("\\", "/")
            if isdir(check_dir_exist) and file != '__MACOSX':   #handle for mac hidden file
                temp_obj = Files(self.resolution, check_dir_exist, self.output_directory)
                status = temp_obj.genoutputfiles()
                print("look in zip folder status {}".format(status))
            else:
                self.convert2image(file)

        return True

    def convert2image(self, file):
        try:
            file_name, extension = splitext(file)
            extension = extension.lower()

            if 'pdf' in extension:
                self.pdf2png(self.input_directory, file_name)
            elif 'docx' in extension or 'doc' in extension:
                # docx2pdf2(self.input_directory,file_name,extension)
                self.docx2image(self.input_directory, file_name, extension)
            elif 'zip' in extension:
                self.zip2png(file, file_name)
            elif 'jpg' in extension or 'jpeg' in extension:
                if self.resolution>100:
                    img1 = cv2.imread(join(self.input_directory, file))
                    cv2.imwrite(join(self.output_directory, file_name) + ".png" ,img1, [cv2.IMWRITE_JPEG_QUALITY, (self.resolution if self.resolution>100 else 20)])
                else:
                    shutil.copy(join(self.input_directory, file), self.output_directory)
            elif 'png' in extension:
                file_path = join(self.input_directory, file)
                shutil.copy(file_path, self.output_directory)
        except IndexError as e:
            logger.exception(e)
            pass

    def zip2png(self, zipfile, zip_name):

        temp_dir = zip_name + '_temp'
        temp_path = join(self.input_directory, temp_dir).replace("\\", "/")

        with ZipFile(join(self.input_directory, zipfile).replace("\\", "/"),'r') as zip:
            directory_to_extract_to = make_directory(temp_path)
            zip.extractall(directory_to_extract_to)
            zip.close()

        temp_obj = Files(self.resolution,temp_path,self.output_directory)
        status = temp_obj.genoutputfiles()
        logger.info(status)

        try:
            if exists(temp_path):
                shutil.rmtree(temp_path)
                os.rmdir(temp_path)
        except FileNotFoundError:
            logger.info("Wrong file or file path")

        return True

    def pdf2png(self, directory, pdf_name):
        """poppler_path required for windows"""
        file = join(directory, pdf_name)
        pdf = PyPDF2.PdfFileReader(file + '.pdf')

        try:
            for page in range(pdf.getNumPages()):
                time_start1 = time.time()
                pgnum = page + 1
                pdfwrite = PdfFileWriter()
                pdfwrite.addPage(pdf.getPage(page))
                outputfilename = '{}_page_{}.pdf'.format(
                    pdf_name, pgnum)
                outputfile = join(self.output_directory, outputfilename)
                with open(outputfile, 'wb') as out:
                    pdfwrite.write(out)

                if isfile(outputfile):
                    if get_env() == 'Production':
                        page = convert_from_path(outputfile, dpi=500)
                    else:
                        """specified poppler path required for windows"""
                        page = convert_from_path(outputfile, dpi=500,
                                          poppler_path=r"C:\Users\kaiboey2\Downloads\Release-21.10.0-0\poppler-21.10.0\Library\bin")

                    page[0].save(join(self.output_directory, pdf_name) + "_{}.png".format(pgnum), 'PNG')
                    os.remove(outputfile)

                time_end1 = time.time()
                print("pdf2png convert pdf to image page {} time =".format(pgnum, time_end1 - time_start1))
        except IndexError as e:
            logger.exception(e)
            return False

        return True

    def docx2image(self,directory,docx_name,extension):

        try:
            output_file_name = "{}.pdf".format(docx_name)
            input_file = join(directory, docx_name+extension).replace("\\", "/")
            output_file = join(directory, output_file_name).replace("\\", "/")
            convert(input_file, output_file)
            self.pdf2png(directory, output_file_name)
            os.remove(output_file)
        except IndexError as e:
            logger.exception(e)
            return False

        return True

    # def pdf2png(self, directory, pdf_name):
    #     """poppler_path required for windows"""
    #     try:
    #         time_start1 = time.time()
    #         if get_env() == 'Production':
    #             pages = convert_from_path(join(directory, pdf_name + '.pdf'), dpi=self.resolution)
    #         else:
    #             pages = convert_from_path(join(directory, pdf_name+'.pdf'), dpi=self.resolution, poppler_path = r"C:\Users\kaiboey2\Downloads\Release-21.10.0-0\poppler-21.10.0\Library\bin")
    #         time_end1 = time.time()
    #         logger.info("pdf2png convert pdf time =", time_end1 - time_start1)
    #         time_start2 = time.time()
    #         for idx, page in enumerate(pages):
    #             page.save(join(self.output_directory, pdf_name) + "_{}.png".format(idx), 'PNG')
    #         time_end2 = time.time()
    #         logger.info("pdf2png save pdf time =", time_end2 - time_start2)
    #     except IndexError as e:
    #         logger.exception(e)
    #         return False
    #
    #     return True


