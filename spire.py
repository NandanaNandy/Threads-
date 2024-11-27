from spire.pdf.common import *
from spire.pdf import *
doc = PdfDocument()
doc.LoadFromFile("E:\\sample docs\\html cheatsheet.pdf")

for i in range(doc.Pages.Count):

    fileName = "Output/img-{0:d}.png".format(i)
    with doc.SaveAsImage(i) as imageS:
        imageS.Save(fileName)

doc.Close()