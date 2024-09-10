from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import *
from .forms import *
import logging

logger = logging.getLogger(__name__)


class TypeListView(ListView):
  model = CostType
  template_name = "costtype/list.html"
  success_url = reverse_lazy('costtype:list')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["function_no"] = 5
    return context


class TypeUpdateView(UpdateView):
  model = CostType
  form_class = TypeForm
  template_name = "costtype/update.html"
  success_url = reverse_lazy('costtype:list')

  def get_object(self, queryset=None):
    pk = self.kwargs['pk']
    logger.debug("TypeUpdateView.get_object pk = " + str(pk))
    if pk == 0:
      obj = None
    else:
      obj = CostType.objects.get(pk=pk)
    return obj

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["function_no"] = 5
    return context


def delete(request, pk):
  logger.debug("delete pk = " + str(pk))
  obj = CostType.objects.filter(pk=pk).delete()
  return redirect('costtype:list')
