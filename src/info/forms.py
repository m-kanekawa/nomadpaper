from django import forms
from .models import Info


class InfoForm(forms.ModelForm):
  class Meta:
    model = Info
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super(InfoForm, self).__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs["class"] = 'form-control'
