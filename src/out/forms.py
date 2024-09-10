from datetime import date
from django import forms
from .models import Out
from costtype.models import CostType


class OutForm(forms.ModelForm):
  class Meta:
    model = Out
    fields = ['date_paid', 'title', 'region', 'cost_type', 'tax_rate', 'net', 'vat', 'vat21', 'vat9', 'total', 'reciept', 'memo']
    date_paid = forms.DateField(
      input_formats=['%Y/%m/%d']
    )

  def __init__(self, *args, **kwargs):
    super(OutForm, self).__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs["class"] = 'form-control'
    self.fields['date_paid'].initial           = date.today()
    self.fields['date_paid'].widget.input_type = 'date'
    self.fields['memo'].widget.attrs['rows']   = 4
