from django.views.generic import ListView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import Avg, Sum, Max, Min, Count, Q
from datetime import date
import math
from .models import VatReport
from income.models import Income
from out.models import Out
from nomadpaper.q import *
import logging

logger = logging.getLogger(__name__)


class VatListView(ListView):
  model = VatReport
  ordering = ['-year', '-q'] 
  template_name = "vat/list.html"
  success_url = reverse_lazy('vat:list')

  def get_context_data(self, **kwargs):
    try:
      vat = VatReport.objects.order_by('-year', '-q').first()
      year = vat.year if vat.q < 4 else vat.year + 1
      q    = vat.q + 1 if vat.q < 4 else 1

    except:
      year = date.today().year
      q    = getCurrentQ()

    context = super().get_context_data(**kwargs)
    context["function_no"] = 6
    context["next"]        = {"year":year, "q":q}
    return context


class VatCreateView(TemplateView):
  template_name = "vat/detail.html"

  def get_context_data(self, **kwargs):
    year = self.kwargs['year']
    q    = self.kwargs['q']
    logger.debug('VAT.get_context_data ' + str(year) + '/' + str(q))

    try:
      vat = VatReport.objects.get(year=year, q=q)
      data = {
        't1a' : vat.net_1_a,
        'b1a' : vat.btw_1_a,
        't1b' : vat.net_1_b,
        'b1b' : vat.btw_1_b,
        't1e' : vat.net_1_e,
        't3a' : vat.net_3_a,
        't3b' : vat.net_3_b,
        't4a' : vat.net_4_a,
        'b4a' : vat.btw_4_a,
        't4b' : vat.net_3_b,
        'b4b' : vat.btw_4_b,
        'b5a' : vat.btw_5_a,
        'b5b' : vat.btw_5_b,
        'b5c' : vat.btw_5_c,
        'b5g' : vat.btw_5_g,
      }
      save = False

    except:
      start_date, end_date = getQdate(year, q)
      logger.debug('start_date = ' + str(start_date))
      logger.debug('end_date = ' + str(end_date))

      t1a = Income.objects.filter(region=1, date__range=(start_date, end_date)).aggregate(r=Sum('net21'))['r'] or 0
      b1a = Income.objects.filter(region=1, date__range=(start_date, end_date)).aggregate(r=Sum('vat21'))['r'] or 0
      t1b = Income.objects.filter(region=1, date__range=(start_date, end_date)).aggregate(r=Sum('net9'))['r'] or 0
      b1b = Income.objects.filter(region=1, date__range=(start_date, end_date)).aggregate(r=Sum('vat9'))['r'] or 0
      t1e = Income.objects.filter(region=1, date__range=(start_date, end_date)).aggregate(r=Sum('net0'))['r'] or 0

      t3a = Income.objects.filter(region=3, date__range=(start_date, end_date)).aggregate(r=Sum('total'))['r'] or 0
      t3b = Income.objects.filter(region=2, date__range=(start_date, end_date)).aggregate(r=Sum('total'))['r'] or 0
      t4a = Out.objects.filter(region=3, date_paid__range=(start_date, end_date)).aggregate(r=Sum('net'))['r'] or 0
      b4a = t4a * 0.21
      t4b = Out.objects.filter(region=2, date_paid__range=(start_date, end_date)).aggregate(r=Sum('net'))['r'] or 0
      b4b = t4b * 0.21

      t5a = Out.objects.filter(~Q(region=1), date_paid__range=(start_date, end_date)).aggregate(r=Sum('net'))['r'] or 0
      b5a = t5a * 0.21

      t5b_region1 = Out.objects.filter(region=1, date_paid__range=(start_date, end_date)).aggregate(r=Sum('vat'))['r'] or 0
      b5b = t5b_region1 + b5a
      b5c = b5g = math.ceil(b5a) - math.ceil(b5b)
  
      data = {
        't1a' : math.ceil(t1a),
        'b1a' : math.ceil(b1a),
        't1b' : math.ceil(t1b),
        'b1b' : math.ceil(b1b),
        't1e' : math.ceil(t1e),
        't3a' : math.ceil(t3a),
        't3b' : math.ceil(t3b),
        't4a' : math.ceil(t4a),
        'b4a' : math.ceil(b4a),
        't4b' : math.ceil(t4b),
        'b4b' : math.ceil(b4b),
        'b5a' : math.ceil(b5a),
        'b5b' : math.ceil(b5b),
        'b5c' : b5c,
        'b5g' : b5g,
      }
      save = True

    context = super().get_context_data(**kwargs)
    context["function_no"] = 6
    context["d"]           = data
    context["save"]        = save
    return context


  def post(self, request, year, q):
    logger.debug('VAT.post ' + str(year) + '/' + str(q))
    vat, created = VatReport.objects.get_or_create(year=year, q=q)
    vat.net_1_a  = float(request.POST["t1a"])
    vat.btw_1_a  = float(request.POST["b1a"])
    vat.net_1_b  = float(request.POST["t1b"])
    vat.btw_1_b  = float(request.POST["b1b"])
    vat.net_1_e  = float(request.POST["t1e"])
    vat.net_3_a  = float(request.POST["t3a"])
    vat.net_3_b  = float(request.POST["t3b"])
    vat.net_4_a  = float(request.POST["t4a"])
    vat.btw_4_a  = float(request.POST["b4a"])
    vat.net_4_b  = float(request.POST["t4b"])
    vat.btw_4_b  = float(request.POST["b4b"])
    vat.btw_5_a  = float(request.POST["b5a"])
    vat.btw_5_b  = float(request.POST["b5b"])
    vat.btw_5_c  = float(request.POST["b5c"])
    vat.btw_5_g  = float(request.POST["b5g"])
    vat.save()
    return redirect('vat:list')


def delete(request, year, q):
  logger.debug("delete year = " + str(year) + ' q = ' + str(q))
  obj = VatReport.objects.filter(year=year, q=q).delete()
  return redirect('vat:list')
