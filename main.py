import fitz

def convertToPng(file):
    try:
        doc = fitz.open(file)
        page_count = len(doc)
        for idx in range(page_count):
            page = doc.loadPage(idx)  # number of page
            pix = page.getPixmap()
            output = "outfile{}.png".format(idx)
            pix.writePNG(output)
    except:
        print("File exception")

def main():
    myfile = "Question 3_LIANG Qihang_55917602.pdf"
    convertToPng(myfile)

if __name__ == "__main__":
    main()

