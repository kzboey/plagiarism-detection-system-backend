import io
from base64 import encodebytes
from PIL import Image
from flask import jsonify
import base64
from utils.uuidgenerator import gen_uuid4
import cv2


def convert_base64(file):

    if file is None:
        return 0

    # image_file = Image.open(file)
    # temp_file = gen_uuid4()+'.png'
    # image_file.save(temp_file, optimize=True, quality=10)
    with open(file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        encoded_base64 = encoded_string.decode("utf-8")

    # os.remove(temp_file)
    return encoded_base64

def get_response_image(image_path):

    pil_img = Image.open(image_path, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img


def get_images(image_lists):
    ##reuslt  contains list of path images
    encoded_imges = []
    for image_path in image_lists:
        encoded_imges.append(get_response_image(image_path))
    return jsonify(encoded_imges)

def resize_images(image):
    width = 3072
    height = 4096   #3.2 times low res image
    points = (width, height)
    resized_image = cv2.resize(image, points)
    return resized_image

def resize_images_low(image):
    width = 960
    height = 1280
    points = (width, height)
    resized_image = cv2.resize(image, points)
    return resized_image