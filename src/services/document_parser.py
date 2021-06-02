import os
import docx

class DocumentParser():
    def __init__(self, filename):
        if not os.path.exists(filename := os.path.abspath(filename)):
            raise docx.opc.exceptions.PackageNotFoundError("Invalid path to the file with the document")

        self.filename = filename
        self.document = docx.Document(self.filename)

    def printall(self, version):
        document = self.document
        for t in document.tables:
            for x in t.rows:
                for y in x.cells:
                    print(y.text)

    def save(self):
        self.document.save()
