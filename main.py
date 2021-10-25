from utils.fileutils import Files

from utils.uuidgenerator import gen_uuid4,random_id

def main():
    #testing fucntion
    #genoutputfiles()
    random_id()
    random_id(4)
    fileutl = Files(resolution=200)
    fileutl.genoutputfiles()

if __name__ == "__main__":
    main()

