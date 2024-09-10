from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .models import *
from .forms import *
import logging

logger = logging.getLogger(__name__)


class InfoUpdateView(UpdateView):
  model = Info
  form_class = InfoForm
  template_name = "info/update.html"
  success_url = reverse_lazy('board:show')

  def get(self, request, *args, **kwargs):
    pk = self.kwargs['pk']
    line, created = Info.objects.get_or_create(pk=pk)
    return super().get(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["function_no"] = 7
    return context
