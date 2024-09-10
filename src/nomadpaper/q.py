from datetime import date

def getCurrentQdate(month, year):
  if month <= 3:
    start_date = date(year, 1, 1)
    end_date   = date(year, 3, 31)
  elif month <= 6:
    start_date = date(year, 4, 1)
    end_date   = date(year, 6, 30)
  elif month <= 9:
    start_date = date(year, 7, 1)
    end_date   = date(year, 9, 30)
  elif month <= 12:
    start_date = date(year, 10, 1)
    end_date   = date(year, 12, 31)
  return start_date, end_date

def getPriviousQdate(month, year):
  if month <= 3:
    start_date = date(year-1, 10, 1)
    end_date   = date(year-1, 12, 31)
  elif month <= 6:
    start_date = date(year, 1, 1)
    end_date   = date(year, 3, 31)
  elif month <= 9:
    start_date = date(year, 4, 1)
    end_date   = date(year, 6, 30)
  elif month <= 12:
    start_date = date(year, 7, 1)
    end_date   = date(year, 9, 30)
  return start_date, end_date
  
def getQdate(year, q):
  if q == 1:
    start_date = date(year, 1, 1)
    end_date   = date(year, 3, 31)
  elif q == 2:
    start_date = date(year, 4, 1)
    end_date   = date(year, 6, 30)
  elif q == 3:
    start_date = date(year, 7, 1)
    end_date   = date(year, 9, 30)
  elif q == 4:
    start_date = date(year, 10, 1)
    end_date   = date(year, 12, 31)
  return start_date, end_date

def getCurrentQ():
    m = date.today().month
    if m <= 3:
      return 1
    elif m <= 6:
      return 2
    elif m <= 9:
      return 3
    elif m <= 12:
      return 4