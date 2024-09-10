from datetime import date
from django.shortcuts import render
from django.db.models import Avg, Sum, Max, Min, Count
from income.models import Income
from out.models import Out
import logging

logger = logging.getLogger(__name__)



def show(request):
  if request.method == 'GET':
    years_query  = Out.objects.dates('date_paid', 'year').distinct()
    years        = [x.year for x in years_query]
    years_sorted = sorted(years, reverse=True)

    data = []
    for year in years_sorted:
      start_date = date(year, 1, 1)
      end_date   = date(year, 12, 31)
      o   = Out.objects.filter(date_paid__range=(start_date, end_date)).aggregate(sum_total=Sum("total"))['sum_total'] or 0
      i   = Income.objects.filter(date__range=(start_date, end_date)).aggregate(sum_total=Sum("total"))['sum_total'] or 0
      data.append( {'year': year, 'in': i, 'out':o} )
      logger.debug(str(year) + ':' + str(i)+ ':' + str(o))

    in_total  = Income.objects.aggregate(total=Sum('total'))['total']
    out_total = Out.objects.aggregate(total=Sum('total'))['total']

    context = {
      'function_no': 1,
      'in_total'   : in_total,
      'out_total'  : out_total,
      'data'       : data
    }
    return render(request, 'board/index.html', context)
