# albums/forms.py
from django import forms

class ArrayForm(forms.Form):
    array_data = forms.CharField(widget=forms.Textarea, label='Enter Albums')
