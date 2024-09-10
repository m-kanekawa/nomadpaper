import datetime
from enum import IntEnum
import unicodedata


#全角=2 半角=1で文字数カウント
def string_width(string):
    width = 0
    for c in string:
        char_width = unicodedata.east_asian_width(c)
        if char_width in u"WFA":
            width += 2
        else:
            width += 1

    return width

#全角=2 半角=1で文字数カウントした文字位置を取得
def get_string_pos(string, n):
    width = 0
    pos = 0
    for c in string:
        char_width = unicodedata.east_asian_width(c)
        if char_width in u"WFA":
            width += 2
        else:
            width += 1
        if width > n:
            return pos
        pos += 1

    return pos
