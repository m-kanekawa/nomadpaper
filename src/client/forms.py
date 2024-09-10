from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
  class Meta:
    model = Client
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super(ClientForm, self).__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs["class"] = 'form-control'
