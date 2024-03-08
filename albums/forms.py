# albums/forms.py
from django import forms

class ArrayForm(forms.Form):
    # TODO: Remove this.. not being used..
    array_data = forms.CharField(widget=forms.Textarea)
