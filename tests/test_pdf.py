import os

from django.test import SimpleTestCase

from helpers.pdf import PDF


class MyPDF(PDF):
    f = 'mypdf.pdf'
    def draw_table(self):
        self.table([
            ['regel 1', '1'],
            ['regel 2', '2']
        ], [2, 2])

        self.table([['tweecellig', 'wezen']], [2, 2], x=10)

    def draw_line(self):
        self.line(0, 0, 10, 10)

    def draw_par(self):
        self.wrapped_text('Heel lang verhaal met veel tekst', width=5, y=10)

        self.wrapped_text(['meerdere', 'regels'], width=5, height=5, y=15)

    def draw_rect(self):
        self.rect(2, 2, 4, 4, color=(0.8, 0.7, 0.0))

    def filename(self):
        return self.f


class MyWidePDF(MyPDF):
    def draw_table(self):
        self.table([
            ['regel 1', '1'],
            ['regel 2', '2']
        ], [20, 20], style=[
            ('FONT', (0, 0), (-1, -1), self.font),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
        ])

        self.table([
            ['regel 1', '1'],
            ['regel 2', '2'],
        ], [2, 2], rowHeights=[20, 20])

        self.table([
            ['regel 1', '1'],
            ['regel 2', '2'],
        ], [2, 2], rowHeights=10)

        self.string('The quick brown fox jumped over the lazy dog')


class PdfTest(SimpleTestCase):
    def test_pdf(self):
        pdf = PDF()

        pdf.write_pdf('/tmp')
        filepath = os.path.exists(os.path.join('/tmp', pdf.filename()))
        self.assertTrue(filepath)

    def test_http_response(self):
        pdf = PDF()

        response = pdf.http_response()

    def test_simple_doc(self):
        pdf = MyPDF()
        pdf.write_pdf('/tmp')

        filepath = os.path.exists(os.path.join('/tmp', pdf.filename()))
        self.assertTrue(filepath)

    def test_set_margins(self):
        pdf = MyPDF()
        pdf.set_top_margin(5)
        pdf.set_left_margin(0.5)
        pdf.f = 'mypdf-margins.pdf'
        pdf.write_pdf('/tmp')

        filepath = os.path.exists(os.path.join('/tmp', pdf.filename()))
        self.assertTrue(filepath)

    def test_width(self):
        'should print a warning to stdout that the table exceeds the margins'
        pdf = MyWidePDF()
        pdf.write_pdf('/tmp')
