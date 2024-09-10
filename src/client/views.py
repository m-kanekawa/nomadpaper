from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import *
from .forms import *
import logging

logger = logging.getLogger(__name__)


class ClientListView(ListView):
  model = Client
  form_class = ClientForm
  template_name = "client/list.html"
  success_url = reverse_lazy('client:list')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["function_no"] = 4
    return context


class ClientUpdateView(UpdateView):
  model = Client
  form_class = ClientForm
  template_name = "client/update.html"
  success_url = reverse_lazy('client:list')

  def get_object(self, queryset=None):
    pk = self.kwargs['pk']
    logger.debug("ClientUpdateView.get_object pk = " + str(pk))
    if pk == 0:
      obj = None
    else:
      obj = Client.objects.get(pk=pk)
    return obj

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["function_no"] = 4
    return context


def delete(request, pk):
  logger.debug("delete pk = " + str(pk))
  obj = Client.objects.filter(pk=pk).delete()
  return redirect('client:list')
