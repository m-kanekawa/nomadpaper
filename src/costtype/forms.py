from django import forms
from django.forms.widgets import Input, TextInput
from .models import CostType
import logging

logger = logging.getLogger(__name__)


class ColorSelect(Input):
  input_type = "text"
  template_name = "widgets/color_select.html"

  def __init__(self, attrs=None, choices=(), *args, **kwargs):
    self.choices = choices
    super(ColorSelect, self).__init__(attrs)

  def get_context(self, name, value, attrs):
    context = super().get_context(name, value, attrs)
    context["widget"]["choices"] = self.choices
    context["widget"]["default_color"] = self.choices[1][0]
    logger.debug("choices" + str(self.choices[1][0]))
    return context


class TypeForm(forms.ModelForm):
  class Meta:
    model = CostType
    fields = '__all__'
    widgets = {
        'color': ColorSelect(choices=CostType.COLOR_CHOICES),
    }


def __init__(self, *args, **kwargs):
  super(TypeForm, self).__init__(*args, **kwargs)
  for field in self.fields.values():
    field.widget.attrs["class"] = 'form-control'
