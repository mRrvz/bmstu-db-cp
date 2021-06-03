""" """

import os
import docx

import db.models as models

class DocumentParser():
    def __init__(self, filename):
        if not os.path.exists(filename := os.path.abspath(filename)):
            raise docx.opc.exceptions.PackageNotFoundError("Invalid path to the file with the document")

        self.filename = filename
        self.document = docx.Document(self.filename)

    def discipline_base(self):
        iterator = BaseInfoIterator(self.document)
        fields = [None] + [field for field in iterator]
        return models.DisciplineWorkProgram(*fields)

    def learning_outcomes(self):
        pass

    def educational_program(self):
        pass

    def discipline_scope(self):
        pass

    def discipline_module(self):
        pass

    def discipline_materials(self):
        pass

    def get_discipline_program(self):
        base = discipline_base()

    def printall(self, version):
        document = self.document
        for t in document.tables:
            for x in t.rows:
                for y in x.cells:
                    print(y.text)

    def save(self):
        self.document.save()


class BaseInfoIterator():
    def __iter__(self):
        return self

    def __init__(self, document):
        self.document = document

        self.counter = 0
        self.trigger_index = 0
        self.triggers = (
            lambda x: "рабочая программа дисциплины" not in x,
            lambda x: "автор программы:" not in x,
            lambda x: not x.endswith("+"),
        )

        self.offsets = (lambda: +1, lambda: +1, lambda: +0)
        self.formatter = (lambda x: x[1:-1], lambda x: x[:x.find(",")], lambda x: x)

    def __next__(self):
        if self.trigger_index >= len(self.triggers):
            raise StopIteration

        paragraphs = self.document.paragraphs
        current_trigger = self.triggers[self.trigger_index]
        current_offset = self.offsets[self.trigger_index]
        current_formatter = self.formatter[self.trigger_index]

        while current_trigger(paragraphs[self.counter].text.lower()):
            self.counter += 1

        self.trigger_index += 1
        return current_formatter(paragraphs[self.counter + current_offset()].text)

