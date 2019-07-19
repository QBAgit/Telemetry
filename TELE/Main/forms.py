from django import forms
from .models import Fdata

class TinyFormTest(forms.ModelForm):
    class Meta:
        model = Fdata
        fields = ("name","description")