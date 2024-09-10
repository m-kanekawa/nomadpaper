from datetime import date
from calendar import monthrange
from django import forms
from django.forms import ModelForm
from .models import Income


class InInfoForm(ModelForm):
  class Meta:
    model = Income
    fields = ['client', 'region', 'number', 'currency', 'date', 'paydue']

  def __init__(self, *args, **kwargs):
    super(InInfoForm, self).__init__(*args, **kwargs)
    today = date.today()
    count = Income.objects.filter(date__year = today.year).count() + 1

    for field in self.fields.values():
      field.widget.attrs["class"] = 'form-control'
    self.fields['number'].initial = "%4d-%04d" % (today.year, count)
    self.fields['date'].initial   = today
    self.fields['paydue'].initial = today.replace(day=monthrange(today.year, today.month)[1])


class InStatusForm(ModelForm):
  class Meta:
    model = Income
    fields = ['status']

  def __init__(self, *args, **kwargs):
    super(InStatusForm, self).__init__(*args, **kwargs)

    for field in self.fields.values():
      field.widget.attrs["class"] = 'form-control'

