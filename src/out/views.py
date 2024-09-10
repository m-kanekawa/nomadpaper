from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import Sum
from datetime import date
from .models import Out
from .forms import OutForm
from nomadpaper.q import getCurrentQdate, getPriviousQdate
import logging

logger = logging.getLogger(__name__)


class OutListView(ListView):
  model         = Out
  ordering      = ['-date_paid']
  template_name = "out/list.html"
  success_url   = reverse_lazy('out:list')

  def get_context_data(self, **kwargs):
    years        = Out.objects.dates('date_paid', 'year').distinct()
    years_sorted = ['Year ' + str(x.year) for x in years]
    years_sorted.sort(reverse=True)

    context = super().get_context_data(**kwargs)
    context["function_no"] = 3
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

    logger.debug("OutListView.get_queryset filter = " + str_filter)
  
    if str_filter != 'ANY':
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

      queryset = queryset.filter(date_paid__range=(start_date, end_date))

    self.filter = str_filter
    self.total  = queryset.aggregate(sum_total=Sum("total"))['sum_total'] or 0
    self.vat    = queryset.aggregate(vat_total=Sum("vat"))['vat_total'] or 0

    return queryset


class OutUpdateView(UpdateView):
  model = Out
  form_class = OutForm
  template_name = "out/update.html"
  success_url = reverse_lazy('out:list')

  def get_object(self, queryset=None):
    pk = self.kwargs['pk']
    if pk == 0:
      obj = None
    else:
      obj = Out.objects.get(pk=pk)
    self.obj = obj
    return obj

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["function_no"] = 3
    context["out"]         = self.obj
    return context

  def form_valid(self, form):
    f = self.request.FILES.get('reciept')
    if (f == None) and (self.obj != None) and (self.obj.reciept != ''):
      logger.debug("remove reciept pk=" + str(self.obj.pk) +  "name=" + str(self.obj.reciept))
      self.obj.reciept.delete()

    return super().form_valid(form)


def delete(request, pk):
  logger.debug("delete pk = " + str(pk))
  obj = Out.objects.filter(pk=pk).delete()
  return redirect('out:list')
