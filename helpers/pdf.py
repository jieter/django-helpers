import copy
from email.mime.application import MIMEApplication

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph, Table
from six import StringIO

from .views import pdf_response

styles = getSampleStyleSheet()


def cm_to_units(l):
    return map(lambda x: x * cm, l)


class PDF(object):
    '''
    Allows drawing a PDF without worrying about units: everything is in centimeters
    with axis orig in top left corner of document
    '''
    paragraph_style = copy.deepcopy(styles['Normal'])
    small_style = copy.deepcopy(styles['Normal'])
    constrast_color = (0.6, 0.6, 1)

    font = 'Helvetica'
    colors = colors

    left_margin = 2
    right_margin = 1.5
    top_margin = 1.9
    bottom_margin = 1

    debug = False

    def __init__(self, pagesize=A4):
        self.pagesize = pagesize
        self.width = pagesize[0] / cm
        self.height = pagesize[1] / cm

        self.small_style.fontSize = 9

        if self.debug:
            for style in [self.paragraph_style, self.small_style]:
                style.borderWidth = 0.1
                style.borderColor = 'red'

    def set_top_margin(self, size):
        self.top_margin = size

    def set_left_margin(self, size):
        self.left_margin = size

    def wrap_width(self, width=None):
        if width is None:
            width = self.width - self.left_margin - self.right_margin

        return width * cm

    def wrap_height(self, height=None):
        if height is None:
            height = self.height - self.top_margin - self.bottom_margin

        return height * cm

    def paragraph(self, text, style=None):
        if isinstance(text, (list, tuple)):
            text = '<br />'.join(text)
        style = style or self.paragraph_style
        return Paragraph(text, style)

    def wrap(self, obj, width=None, height=None):
        return obj.wrapOn(self.canvas, self.wrap_width(width), self.wrap_height(height))

    def wrapped_text(self, text, x=None, y=None, width=None, height=None, style=None, anchor='top'):
        x = (x or self.left_margin) * cm
        y = -(y if y is not None else self.top_margin) * cm

        par = self.paragraph(text, style)
        dx, dy = self.wrap(par, width, height)
        par.drawOn(self.canvas, x, y - dy if anchor == 'top' else y)
        return dx / cm, dy / cm

    def table(self, data, colWidths, rowHeights=None, style=None, x=None, y=None, width=None, height=None):
        # check if table width falls between margins if table starts at left margin
        if x is None or x == self.left_margin:
            to_wide = sum(colWidths) - (self.width - self.left_margin - self.right_margin)
            if to_wide > 0:
                print('Table outside page margins by %0.2fcm' % to_wide)

        x = (x or self.left_margin) * cm
        y = -(y if y is not None else self.top_margin) * cm

        kwargs = {}
        if rowHeights:
            if not isinstance(rowHeights, list):
                rowHeights = [rowHeights] * int(len(data))
            kwargs['rowHeights'] = cm_to_units(rowHeights)

        table = Table(data, cm_to_units(colWidths), **kwargs)
        if style:
            table.setStyle(style)

        dx, dy = self.wrap(table, width, height)
        table.drawOn(self.canvas, x, y - dy)
        return dx / cm, dy / cm

    def line(self, x0, y0, x1, y1, width=1, color=None):
        color = color or self.constrast_color

        self.canvas.setStrokeColorRGB(*color)
        self.canvas.setLineWidth(width)
        self.canvas.line(x0 * cm, -y0 * cm, x1 * cm, -y1 * cm)

    def rect(self, x0, y0, x1, y1, color=None):
        color = color or self.constrast_color

        self.canvas.setFillColorRGB(*color)
        self.canvas.rect(x0 * cm, -y0 * cm, x1 * cm, -y1 * cm, fill=True)

    def string(self, string, x=None, y=None, font_size=10):
        x = (x or self.left_margin) * cm
        y = -(y if y is not None else self.top_margin) * cm

        self.canvas.setFont(self.font, font_size)
        self.canvas.drawString(x, y, string)

    def guarded_draw(self, draw_function):
        self.canvas.saveState()
        draw_function()
        self.canvas.restoreState()

    def draw(self, canvas):
        self.canvas = canvas

        for func in dir(self):
            if func.startswith('draw_'):
                self.guarded_draw(getattr(self, func))

        self.canvas.showPage()
        self.canvas.save()

    def filename(self):
        return 'document.pdf'

    def write_to(self, buf):
        canvas = Canvas(buf, pagesize=self.pagesize)
        canvas.translate(0, self.height * cm)
        canvas.setFont(self.font, 10)

        self.draw(canvas)

    def write_pdf(self, path):
        filename = path + '/' + self.filename()
        with file(filename, 'wb') as pdf:
            self.write_to(pdf)

        return filename

    def http_response(self):
        return pdf_response(self)

    def email_attachment(self):
        buf = StringIO()
        self.write_to(buf)
        buf.seek(0)

        attachment = MIMEApplication(buf.read())
        attachment.add_header("Content-Disposition", "attachment",
                              filename=self.filename())
        buf.close()

        return attachment
