import os
from django.conf import settings
from .common import *
from .reportlabEx import *
import logging

logger = logging.getLogger(__name__)

# R1C_TTF = settings.STATIC_ROOT + "/font/rounded-mplus-1c-regular.ttf"
R1C_TTF = str(settings.BASE_DIR) + "/static/font/rounded-mplus-1c-regular.ttf"
MARGIN      = 15
WIDTH       = 210                    # Paper Size X
HEIGHT      = 297                    # Paper Size Y
PAD         = 3                      # Padding between line and string
MARGIN_BETWEEN = 10                  # Y margin between items
L           = MARGIN                 # West  =15
R           = WIDTH - MARGIN         # East  =195
N           = HEIGHT - MARGIN        # North
S           = MARGIN                 # South
W           = WIDTH - MARGIN * 2     # Witdh =180
H           = HEIGHT - MARGIN * 2    # Height =267
X1          = MARGIN                 # table Col 1 X
X2          = 110                    # table Col 2 X
X3          = 132                    # table Col 3 X
X4          = 152                    # table Col 4 X
X5          = 178                    # table Col 5 X
LINE_H_10   = 10
LINE_H_6    = 6
LINE_H_5    = 5
LINE_H_4    = 4
COLOR_1     = '#000000'
COLOR_2     = '#22ac8a'
M_LIST      = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def toDate(date):
  if date == None:
    return ''
  else:
    return str(date.year) + ' ' + M_LIST[date.month-1] + ' ' + str(date.day)

def toCommaD(number):
  return "{:,d}".format(int(number))

def toCommaF(income, number):
  if income.digit == 0:
    return toCommaD(number)
  else:
    strf = "{:,." + income.digit + "f}"
    return strf.format(number)

# def toCommaF(number):
#   strF = "{:,.2f}".format(number)
#   if strF.endswith(".00"):
#     return "{:,.0f}".format(number)
#   else:
#     return strF


class PdfDocument(object):
  def __init__(self, info, client, income, lines):
    registerFont(TTFont('rounded', R1C_TTF))
    self.create(info, client, income, lines)

  # ------------
  # public
  # ------------
  def create(self, info, client, income, lines):
    self.mark = income.get_currency_display() + ' '
    self.rl = ReportlabEx()
    h_sum, h_memo = self.getHeight(income)
    page_len = self.pageAll(info, client, income, lines, h_sum, h_memo, 0)         # ページ数算出
    dummy    = self.pageAll(info, client, income, lines, h_sum, h_memo, page_len)  # 描画


  # ------------
  # private
  # ------------
  def getBuffer(self):
    return self.rl.buffer.getvalue()

  def getHeight(self, income):
    y = 0

    y2 = self.drawTableSum(income, y, False)
    h_sum = y - y2
    logger.debug('h_sum =' + str(h_sum))

    y3 = self.drawMemo(income, y, False)
    h_memo = y - y3
    logger.debug('h_memo =' +  str(h_memo))

    return (h_sum, h_memo)

  def pageAll(self, info, client, income, lines, h_sum, h_memo, page_len):
    doExec = True if page_len>0 else False
    pageNo = 1
    y     = self.drawInfo(info, N, doExec) - MARGIN_BETWEEN
    logger.debug('drawInfo =' + str(y))

    y1    = self.drawClient(client, y, doExec)
    logger.debug('drawClient =' + str(y1))

    y2    = self.drawIncomeInfo(income, y, doExec)
    logger.debug('drawIncomeInfo =' + str(y2))

    y = min(y1, y2) - MARGIN_BETWEEN
    line = 0
    while True:
      y, line = self.drawTable(income, lines, y, line, doExec)
      logger.debug('drawTable =' + str(y) + ', ' + str(line))
      if line == len(lines):
        break
      else:
        self.drawPageNo(pageNo, page_len, doExec)
        pageNo += 1
        self.rl.nextpage(doExec)
        y = N

    if y < h_sum:
      pageNo += 1
      self.rl.nextpage(doExec)

    y = self.drawTableSum(income, y, doExec)
    logger.debug('drawTableSum =' + str(y))

    if y < h_memo + MARGIN_BETWEEN:
      pageNo += 1
      self.rl.nextpage(doExec)

    y = self.drawMemo(income, y - MARGIN_BETWEEN, doExec)
    logger.debug('drawMemo =' + str(y))

    self.drawPageNo(pageNo, page_len, doExec)
    self.rl.done(doExec)

    logger.debug('pageNo =' + str(pageNo))
    return pageNo


  def drawInfo(self, info, yTop, doExec):
    self.rl.setFont(12, COLOR_1, doExec)
    y = yTop - LINE_H_6
    self.rl.drawRightString((R - PAD), y, info.company_name, doExec)

    self.rl.setFont(10, COLOR_1, doExec)
    if info.address1 != '':
      y -= LINE_H_5
      self.rl.drawRightString((R - PAD), y, info.address1, doExec)
    if info.address2 != '':
      y -= LINE_H_5
      self.rl.drawRightString((R - PAD), y, info.address2, doExec)
    if info.address3 != '':
      y -= LINE_H_5
      self.rl.drawRightString((R - PAD), y, info.address3, doExec)
    if info.btw != '':
      y -= LINE_H_5
      self.rl.drawRightString((R - PAD), y, "BTW: " + info.btw, doExec)
    if info.kvk != '':
      y -= LINE_H_5
      self.rl.drawRightString((R - PAD), y, "KVK: " + info.kvk, doExec)
    if info.bank != '':
      y -= LINE_H_5
      self.rl.drawRightString((R - PAD), y, "BANK: " + info.bank, doExec)

    yBottom = y - 3
    self.rl.drawLineDeco(R, yBottom, R, yTop, COLOR_2, doExec)
    return yBottom


  def drawClient(self, client, yTop, doExec):
    y = yTop

    if string_width(client.name) <= 50:
      y -= LINE_H_6
      self.rl.setFont(14, COLOR_1, doExec)
    else:
      y -= LINE_H_5
      self.rl.setFont(10, COLOR_1, doExec)

    self.rl.drawString((L + PAD), y, client.nickname, doExec)

    self.rl.setFont(10, COLOR_1, doExec)
    if client.address1 != '':
      y -= LINE_H_5
      self.rl.drawString((L + PAD), y, client.address1, doExec)
    if client.address2 != '':
      y -= LINE_H_5
      self.rl.drawString((L + PAD), y, client.address2, doExec)
    if client.address3 != '':
      y -= LINE_H_5
      self.rl.drawString((L + PAD), y, client.address3, doExec)
    if client.country != '':
      y -= LINE_H_5
      self.rl.drawString((L + PAD), y, client.country, doExec)

    yBottom = y - 3
    self.rl.drawLineDeco(L, yBottom, L, yTop, COLOR_2, doExec)

    return yBottom


  def drawIncomeInfo(self, income, yTop, doExec):
    y = yTop

    self.rl.setFont(14, COLOR_1, doExec)
    y -= LINE_H_6
    self.rl.drawRightString((R - PAD), y, "Invoice " + income.number, doExec)

    self.rl.setFont(10, COLOR_1, doExec)
    y -= LINE_H_5
    self.rl.drawRightString((R - PAD), y, "Invoice date: " + toDate(income.date), doExec)

    y -= LINE_H_5
    self.rl.drawRightString((R - PAD), y, "Payment due: " + toDate(income.paydue), doExec)

    yBottom = y - 3
    self.rl.drawLineDeco(R, yBottom, R, yTop, COLOR_2, doExec)

    return yBottom


  def drawTable(self, income, lines, yTop, line_start, doExec):
    y = yTop - LINE_H_6*2
    self.rl.drawTableTitle(MARGIN, y, W, (LINE_H_6*2), doExec)

    y += LINE_H_6
    self.rl.setFont(9, COLOR_2, doExec)
    self.rl.drawString((X1+PAD), y, "DESCRIPTION", doExec)
    self.rl.drawString(X2, y, "UNIT PRICE", doExec)
    self.rl.drawString(X2, (y - LINE_H_4), "(EX. VAT)", doExec)
    self.rl.drawString(X3, y, "QUANTITY", doExec)
    self.rl.drawString(X4, y, "TOTAL", doExec)
    self.rl.drawString(X4, (y - LINE_H_4), "(EX. VAT)", doExec)
    self.rl.drawString(X5, y, "TAX RATE", doExec)

    y -= LINE_H_6

    self.rl.setFont(9, COLOR_1, doExec)
    i = line_start
    while True:
      y -= LINE_H_10
      if lines[i].title != '':
        self.rl.drawString((X1 + PAD), y, lines[i].title, doExec)
      if lines[i].unit_price != None:
        self.rl.drawRightString((X3 - PAD), y, self.mark + toCommaF(income, lines[i].unit_price), doExec)
      if lines[i].quantity != None:
        self.rl.drawRightString((X4 - PAD), y, 'x ' + toCommaD(lines[i].quantity), doExec)
      if lines[i].total_price != None:
        self.rl.drawRightString((X5 - PAD), y, self.mark + toCommaF(income, lines[i].total_price), doExec)
      if lines[i].tax_rate != None:
        self.rl.drawRightString((R - PAD), y, toCommaD(lines[i].tax_rate) + ' %', doExec)
      i += 1
      if (y - LINE_H_10 < S*2) or (i == len(lines)):
        break

    yBottom = y - 3
    self.rl.drawLineDeco(L, yBottom, L, yTop, COLOR_2, doExec)

    return yBottom, i

  def drawTableSum(self, income, yTop, doExec):
    y = yTop - LINE_H_6 * 2
    self.rl.drawRightString((X4 - PAD), y, "Sub Total", doExec)
    if income.currency==1:
      self.rl.drawRightString((X5 - PAD), y, self.mark + toCommaF(income, income.net), doExec)
    else:
      self.rl.drawRightString((X5 - PAD), y, self.mark + toCommaF(income, income.local_total), doExec)

    y -= LINE_H_6
    self.rl.drawRightString((X4 - PAD), y, "VAT", doExec)
    self.rl.drawRightString((X5 - PAD), y, self.mark + toCommaF(income, income.vat), doExec)
 
    y -= LINE_H_6
    self.rl.drawRightString((X4 - PAD), y, "Total", doExec)
    self.rl.drawRightString((X5 - PAD), y, self.mark + toCommaF(income, income.local_total), doExec)

    yBottom = y - 3
    self.rl.drawLineDeco(L, yBottom, L, yTop, COLOR_2, doExec)

    return yBottom

  def drawMemo(self, income, yTop, doExec):
    memo      = income.memo.replace('\r', '')
    memolines = memo.split('\n')
    memocount = 5

    y = yTop - LINE_H_5
    self.rl.setFont(9, COLOR_2, doExec)
    self.rl.drawString(L, y, "MEMO", doExec)

    self.rl.setFont(9, COLOR_1, doExec)
    for n in range(min(5, len(memolines))):
      y -= LINE_H_5
      self.rl.drawString((L + PAD), y, memolines[n], doExec)

    y = yTop - LINE_H_5 * memocount - LINE_H_5 - PAD
    self.rl.drawRectDeco(MARGIN, y, W, (LINE_H_5 * memocount + PAD), COLOR_2, doExec)
    
    yBottom = y
    return yBottom

  def drawPageNo(self, pageNo, page_len, doExec):
    yBottom = S - 5
    str_page_no = 'Page ' + str(pageNo) + ' / ' + str(page_len)
    self.rl.drawCentredString((MARGIN + (W / 2)), yBottom, str_page_no, doExec)
