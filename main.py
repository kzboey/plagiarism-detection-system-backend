from pdf2image import convert_from_path
import fitz

def main():
    pdffile = "Question 3_LIANG Qihang_55917602.pdf"
    doc = fitz.open(pdffile)
    page_count = len(doc)
    for idx in range(page_count):
        page = doc.loadPage(idx)  # number of page
        pix = page.getPixmap()
        output = "outfile{}.png".format(idx)
        pix.writePNG(output)

if __name__ == "__main__":
    main()