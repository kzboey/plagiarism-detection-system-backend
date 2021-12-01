from docx2pdf import convert
from pdf2image import convert_from_path
from PIL import ImageFile, Image, ExifTags
from zipfile import ZipFile
import os
import shutil
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import current_app
from models.taskmodel import Tasks

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
            file.save(os.path.join(path, filename))
            return True
        else:
            raise Exception("Invalid File Type")
        return False
    except IndexError as e:
        print(e)
        return False


def goto_directory(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)
    os.chdir(dir)

    return os.getcwd()


def get_author(filename):
    author_name = ''
    for element in range(0, len(filename)):
        if filename[element] == '_':
            author_name = filename[:element]
            break
    return author_name


class Files:

    def __init__(self, resolution=600, input_directory=default_input_dir, output_directory=default_output_dir):
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.resolution = resolution

    def genoutputfiles(self):

        dirs = os.listdir(self.input_directory)

        for file in dirs:
            self.convert2image(file)

        return True  #success

    def convert2image(self, file):
        try:
            file_name, extension = os.path.splitext(file)
            extension = extension.lower()

            if 'pdf' in extension:
                self.pdf2png(self.input_directory, file_name)
            elif 'docx' in extension or 'doc' in extension:
                self.docx2pdf(self.input_directory, file_name, extension)
            elif 'zip' in extension:
                self.zip2png(file, file_name)
            elif 'jpg' in extension or 'jpeg' in extension:
                with Image.open(os.path.join(self.input_directory, file)) as im1:
                    im1.save(os.path.join(self.output_directory, file_name) + ".png", 'PNG')
            elif 'png' in extension:
                file_path = os.path.join(self.input_directory, file)
                shutil.copy(file_path, self.output_directory)
        except IndexError as e:
            print(e)
            pass

    def zip2png(self, zipfile, zip_name):
        with ZipFile(os.path.join(self.input_directory, zipfile),'r') as zip:
            temp_dir = zip_name + '_temp'
            temp_path = os.path.join(self.input_directory, temp_dir)
            os.mkdir(temp_path)
            prev_cwd = Path.cwd()
            os.chdir(temp_path)

            for fn in zip.namelist():
                extracted_path = Path(zip.extract(fn))
                extracted_path.rename(fn.encode('cp437').decode('gbk'))

            os.chdir(prev_cwd)
            zip.close()
            temp_obj = Files(input_directory=temp_path)
            status = temp_obj.genoutputfiles()
            print(status)

            if os.path.exists(temp_path):
                shutil.rmtree(temp_path)

        return True

    def pdf2png(self, directory, pdf_name):
        """poppler_path required for windows"""
        try:
            pages = convert_from_path(os.path.join(directory, pdf_name+'.pdf'), dpi=self.resolution, poppler_path = r"C:\Users\kaiboey2\Downloads\Release-21.10.0-0\poppler-21.10.0\Library\bin")
            for idx, page in enumerate(pages):
                page.save(os.path.join(self.output_directory, pdf_name) + "_{}.png".format(idx), 'PNG')
        except IndexError as e:
            print(e)
            return False

        return True

    def docx2pdf(self,directory,docx_name,extension):

        try:
            output_file_name = "{}.pdf".format(docx_name)
            input_file = os.path.join(directory, docx_name+extension)
            output_file = os.path.join(directory, output_file_name)
            convert(input_file, output_file)
            self.pdf2png(directory, docx_name)
            os.remove(output_file)
        except IndexError as e:
            print(e)
            return False

        return True
