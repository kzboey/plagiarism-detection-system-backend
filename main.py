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

def encodebase64(file):

    image_file = Image.open(file)
    image_file.save("temp.png", optimize=True, quality=10)
    with open("temp.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode("utf-8")

def main():
    time_start = time.time()
    file="C:/temp/pages/CS2231_test/chancheukkin/chancheukkin_LATE_146111_6570614_IMG_20201022_151332.png"
    base64_str = convert_base64(file)
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

