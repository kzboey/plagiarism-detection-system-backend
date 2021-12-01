from utils.fileutils import Files
import sys, getopt
from utils.uuidgenerator import gen_uuid4,gen_randomid
from cryptography.fernet import Fernet
import os
import numpy as np


def main():
    # fileutl = Files(resolution=600)
    # fileutl.genoutputfiles()
    np.random.seed(1)
    A_prev = np.random.randn(2,2,2)
    W = np.random.randn(3, 3, 4, 8)
    print(A_prev.shape)
    print(A_prev)
    # (m, n_H_prev, n_W_prev, n_C_prev) = A_prev.shape
    #  (f, f, n_C_prev, n_C) = W

if __name__ == "__main__":
    main()

