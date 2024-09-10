import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import *
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont


class ReportlabEx(object):
  def __init__(self):
    self.buffer = io.BytesIO()
    self.pdf = canvas.Canvas(self.buffer)
    self.pdf.saveState()

  # ------------
  # public
  # ------------
  def nextpage(self, doExec):
    if doExec == False:
      return
    self.pdf.showPage()

  def done(self, doExec):
    if doExec == False:
      return
    self.pdf.showPage()
    self.pdf.save()
    self.buffer.seek(0)

  def setFont(self, size, color, doExec):
    if doExec == False:
      return
    self.__setFillColorRGB(color)
    self.pdf.setFont("rounded", size)

  def drawLineDeco(self, x1,y1, x2,y2, color, doExec):
    if doExec == False:
      return
    self.__setStrokeColorRGB(color) 
    self.pdf.setLineWidth(3)
    self.pdf.setLineCap(1) 
    self.pdf.line(x1 * mm, y1 * mm, x2 * mm, y2 * mm)

  def drawRectDeco(self, x, y, width, height, color, doExec):
    if doExec == False:
      return
    self.__setStrokeColorRGB(color) 
    self.pdf.setLineWidth(1)
    self.__roundRect(x, y, width, height, 3, stroke=1, fill=0)

  def drawTableTitle(self, x, y, width, height, doExec):
    if doExec == False:
      return
    self.pdf.setFillGray(0.9)
    self.__rect(x, y, width, height, stroke=0, fill=1)

  def drawRightString(self, x, y, str, doExec):
    if doExec == False:
      return
    self.pdf.drawRightString(x * mm, y * mm, str)

  def drawString(self, x, y, str, doExec):
    if doExec == False:
      return
    self.pdf.drawString(x * mm, y * mm, str)
  
  def drawCentredString(self, x, y, str, doExec):
    if doExec == False:
      return
    self.pdf.drawCentredString(x * mm, y * mm, str)

  # ------------
  # private
  # ------------
  def __hex_to_rgb1(self, hex):
    h = hex.lstrip('#')
    return tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4))

  def __rect(self, x, y, width, height, stroke, fill):
    self.pdf.rect(x * mm, y * mm, width * mm, height * mm, stroke, fill)

  def __roundRect(self, x, y, width, height, radius, stroke, fill):
    self.pdf.roundRect(x * mm, y * mm, width * mm, height * mm, radius, stroke, fill)

  def __setStrokeColorRGB(self, color):
    rgb = self.__hex_to_rgb1(color)
    self.pdf.setStrokeColorRGB(rgb[0], rgb[1], rgb[2]) 

  def __setFillColorRGB(self, color):
    rgb = self.__hex_to_rgb1(color)
    self.pdf.setFillColorRGB(rgb[0], rgb[1], rgb[2]) 

