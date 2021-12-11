import subprocess
from tkinter import Tk, IntVar, Label, W, Radiobutton, Button, mainloop, TOP, BOTTOM, Frame, LEFT, CENTER, RIGHT, \
    StringVar, OptionMenu
from tkinter.filedialog import askopenfilenames
from PyPDF2 import PdfFileReader, PdfFileWriter
import os

HEADER = './template/kopf.pdf'
BLANK = './template/blank_din4.pdf'
UST_DE = './template/ust-de.pdf'
UST_ENG = './template/ust-eng.pdf'
UST_FRA = './template/ust-fra.pdf'


Tk().withdraw()

filenames = askopenfilenames(defaultextension=".pdf", filetypes=[('pdf file', '*.pdf')])

if not filenames:
    quit()

master = Tk()
master.eval('tk::PlaceWindow . center')
master.geometry('250x150')
var = IntVar(master)
var.set(0)


def quit_loop():
    global chosen_ust
    global selectedPrinter
    selectedPrinter = printer.get()
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
middleFrame = Frame(master)

printerList = subprocess.getoutput("lpstat -p | awk '{print $2}'")
printerList = printerList.split("\n")

printer = StringVar(master)
printer.set(printerList[0])


Label(master, text="Sprache").pack()
Radiobutton(master, text="Deutsch", variable=var, value=0).pack()
Radiobutton(master, text="Englisch", variable=var, value=1).pack()
Radiobutton(master, text="Französisch", variable=var, value=2).pack()

middleFrame.pack()
OptionMenu(middleFrame, printer, *printerList).pack()

bottomFrame.pack()
Button(bottomFrame, text="OK", command=quit_loop).pack(ipadx=15, side=LEFT, padx=10)
Button(bottomFrame, text="Exit", command=quit_program).pack(ipadx=15, side=LEFT)

master.mainloop()

pdfHeader = PdfFileReader(HEADER)
ust = PdfFileReader(chosen_ust)
ust = ust.getPage(0)

for filename in filenames:
    resultFileName = os.path.splitext(filename)[0] + '_EDITED.pdf'
    blank_din4 = PdfFileReader(BLANK)
    blank_din4 = blank_din4.getPage(0)

    with open(resultFileName, 'wb') as resultPdfFile:
        invoice = PdfFileReader(filename)
        blank_din4.mergeScaledTranslatedPage(invoice.getPage(0), 1, 0, -40, True)
        blank_din4.mergeScaledTranslatedPage(pdfHeader.getPage(0), 1, 0, -10, True)
        blank_din4.mergeTranslatedPage(ust, -2, -90, True)
        blank_din4.scaleTo(595, 841)

        pdfWriter = PdfFileWriter()
        pdfWriter.addPage(blank_din4)
a
        for pageNumber in range(1, invoice.numPages):
            pageObj = invoice.getPage(pageNumber)
            pdfWriter.addPage(pageObj)

        pdfWriter.write(resultPdfFile)
        pdfWriter.removeText()

    os.system("lp -d " + selectedPrinter + " -o media=A4 -o fit-to-page " + resultFileName)
    os.remove(filename)
