from django.views.generic import TemplateView, ListView, UpdateView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import Sum
from datetime import date
from .models import *
from info.models import Info
from .forms import *
from .pdf import PdfDocument
from nomadpaper.q import getCurrentQdate, getPriviousQdate
import logging

logger = logging.getLogger(__name__)


class InListView(ListView):
  model         = Income
  ordering      = ['-date']
  template_name = "income/list.html"
  success_url   = reverse_lazy('income:list')

  def get_context_data(self, **kwargs):
    years        = Income.objects.dates('date', 'year').distinct()
    years_sorted = ['Year ' + str(x.year) for x in years]
    years_sorted.sort(reverse=True)

    context = super().get_context_data(**kwargs)
    context["function_no"] = 2
    context["filter"]      = self.filter
    context["net"]         = self.total - self.vat
    context["vat"]         = self.vat
    context["total"]       = self.total
    context["years"]       = years_sorted
    return context

  def get_queryset(self, **kwargs):
    str_filter = self.request.GET.get('filter')
    queryset = super().get_queryset(**kwargs)

    if str_filter == None:
      str_filter = 'Year ' + str(date.today().year)

    if str_filter != 'ANY':
      logger.debug("InListView.get_queryset filter = " + str_filter)

      if str_filter.startswith('Q'):
        year  = date.today().year
        month = date.today().month

        if str_filter == 'QT':
          start_date,end_date = getCurrentQdate(month, year)
        elif str_filter == 'QP':
          start_date,end_date = getPriviousQdate(month, year)
        else:
          logger.debug("ERROR")

      elif str_filter.startswith('Year'):
        year       = str_filter[5:]
        iYear      = int(year)
        start_date = date(iYear, 1, 1)
        end_date   = date(iYear, 12, 31)
      else:
        logger.debug("ERROR")

      queryset = queryset.filter(date__range=(start_date, end_date))

    self.filter = str_filter
    self.total  = queryset.filter(status=3).aggregate(sum_total=Sum("total"))['sum_total'] or 0
    self.vat    = queryset.filter(status=3).aggregate(vat_total=Sum("vat"))['vat_total'] or 0

    return queryset


class InInfoView(UpdateView):
  model         = Income
  form_class    = InInfoForm
  template_name = "income/info.html"
  success_url   = reverse_lazy('income:list')

  def get_object(self, queryset=None):
    pk = self.kwargs['pk']
    if pk == 0:
      obj = None
    else:
      obj = Income.objects.get(pk=pk)
    self.obj = obj
    return obj

  def get_context_data(self, **kwargs):
    pk = self.kwargs['pk']
    context = super().get_context_data(**kwargs)
    context["function_no"] = 2
    if self.obj:
      context["client"] = Client.objects.get(pk=self.obj.client.pk)
    return context


class InStatusView(UpdateView):
  model         = Income
  form_class    = InStatusForm
  template_name = "income/status.html"
  success_url   = reverse_lazy('income:list')

  def get_context_data(self, **kwargs):
    pk = self.kwargs['pk']
    obj = self.get_object()
    logger.debug("obj = " + str(obj.__dict__))

    context = super().get_context_data(**kwargs)
    context["function_no"] = 2
    context["income"]      = obj
    return context

  def post(self, request, pk, **kwargs):
    logger.debug("InStatusView.post")
    saveRate(request, pk)
    return super(InStatusView, self).post(request, **kwargs)


class InDetailView(TemplateView):
  template_name = "income/detail.html"

  def get_context_data(self, **kwargs):
    pk = self.kwargs['pk']
    income = Income.objects.get(pk=pk)
    context = super().get_context_data(**kwargs)
    context["function_no"] = 2
    context["in"]          = income if pk != 0 else None
    context["info"]        = Info.objects.get(pk=1)
    context["client"]      = Client.objects.get(pk=context["in"].client.pk)
    context["lines"]       = getLines(pk)
    context["tax_rates"]   = [
        {'label': label, 'value': value} for value, label in Line._meta.get_field('tax_rate').choices
    ]
    return context

  def post(self, request, pk):
    logger.debug("InDetailView.post pk = " + str(pk))
    saveInfo(request, pk)
    saveLines(request, pk)
    return redirect('income:list')


def to_pdf(request, pk):
  info    = Info.objects.get(pk=1)
  income  = Income.objects.get(pk=pk)
  client  = Client.objects.get(pk=income.client.pk)
  lines   = getLines(pk)
  pdf = PdfDocument(info, client, income, lines)
  # return FileResponse(pdf.buffer, as_attachment=True, filename="invoice.pdf")
  response = HttpResponse(content_type='application/pdf')
  response.write(pdf.getBuffer())
  return response


def getLines(pk):
  return Line.objects.filter(in_id=pk)

def saveRate(request, pk):
  logger.debug('saveRate pk=' + str(pk))
  data = Income.objects.get(pk=pk)
  if data.currency != 1:
    data.rate      = float(request.POST.get("rate") or 0)
    data.total     = float(request.POST.get("total") or 0)
  if data.status == 3:
    data.date_paid = request.POST.get("date_paid")
  data.save()

def saveInfo(request, pk):
  logger.debug('saveInfo pk=' + str(pk))
  data = Income.objects.get(pk=pk)
  data.number      = request.POST.get("number")
  data.date        = request.POST.get("date")
  data.paydue      = request.POST.get("paydue")
  data.memo        = request.POST.get("memo")

  if data.currency == 1: # €
    data.net     = float(request.POST.get("net"))
    data.net0    = float(request.POST.get("net0"))
    data.net9    = float(request.POST.get("net9"))
    data.net21   = float(request.POST.get("net21"))
    data.vat     = float(request.POST.get("vat"))
    data.vat9    = float(request.POST.get("vat9"))
    data.vat21   = float(request.POST.get("vat21"))
    data.total   = float(request.POST.get("total"))
  else:
    data.local_total = float(request.POST.get("total"))
  data.save()

def saveLines(request, in_id):
  logger.debug('saveLines')
  item_cnt = request.POST.get('item_cnt')
  logger.debug('item_cnt = ' + str(item_cnt))
  cnt = int(item_cnt)
  for i in range(1, cnt + 1):
    line, created = Line.objects.get_or_create(in_id=in_id, line_no=i)
    line.title       = '' or request.POST.get('line_' + str(i) + '_title')
    line.unit_price  = 0 or request.POST.get('line_' + str(i) + '_price')
    line.quantity    = 0 or request.POST.get('line_' + str(i) + '_quantity')
    line.total_price = 0 or request.POST.get('line_' + str(i) + '_total')
    line.tax_rate    = 0 or request.POST.get('line_' + str(i) + '_tax_rate')
    line.save()
