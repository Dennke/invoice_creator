from tkinter import Tk, IntVar, Label, W, Radiobutton, Button, mainloop, TOP, BOTTOM, Frame, LEFT, CENTER, RIGHT
from tkinter.filedialog import askopenfilenames
from PyPDF2 import PdfFileReader, PdfFileWriter
import os

HEADER = './.idea/template/kopf.pdf'
BLANK = './.idea/template/blank_din4.pdf'
UST_DE = './.idea/template/ust-de.pdf'
UST_ENG = './.idea/template/ust-eng.pdf'
UST_FRA = './.idea/template/ust-fra.pdf'


Tk().withdraw()

filenames = askopenfilenames(defaultextension=".pdf", filetypes=[('pdf file', '*.pdf')])

if not filenames:
    quit()

master = Tk()
master.geometry('250x150')
var = IntVar(master)
var.set(0)


def quit_loop():
    global chosen_ust
    chosen_ust = UST_DE
    if var.get() == 1:
        chosen_ust = UST_ENG
    if var.get() == 2:
        chosen_ust = UST_FRA
    master.quit()


def quit_program():
    quit()


master.protocol("WM_DELETE_WINDOW", quit_program)

bottomFrame = Frame(master)


Label(master, text="Sprache").pack()
Radiobutton(master, text="Deutsch", variable=var, value=0).pack()
Radiobutton(master, text="Englisch", variable=var, value=1).pack()
Radiobutton(master, text="Französisch", variable=var, value=2).pack()
bottomFrame.pack()
Button(bottomFrame, text="OK", command=quit_loop).pack(ipadx=15, side=LEFT, padx=10)
Button(bottomFrame, text="Exit", command=quit_program).pack(ipadx=15, side=LEFT)

master.mainloop()

pdfHeader = PdfFileReader(HEADER)
ust = PdfFileReader(chosen_ust)
ust = ust.getPage(0)

for filename in filenames:
    resultFileName = os.path.splitext(filename)[0]
    blank_din4 = PdfFileReader(BLANK)
    blank_din4 = blank_din4.getPage(0)

    with open(resultFileName + '_EDITED.pdf', 'wb') as resultPdfFile:
        invoice = PdfFileReader(filename)
        blank_din4.mergeScaledTranslatedPage(invoice.getPage(0), 1, 0, -40, True)
        blank_din4.mergeScaledTranslatedPage(pdfHeader.getPage(0), 1, 0, -10, True)
        blank_din4.mergeTranslatedPage(ust, -2, -90, True)

        pdfWriter = PdfFileWriter()
        pdfWriter.addPage(blank_din4)

        for pageNumber in range(1, invoice.numPages):
            pageObj = invoice.getPage(pageNumber)
            pdfWriter.addPage(pageObj)

        pdfWriter.write(resultPdfFile)
        pdfWriter.removeText()
