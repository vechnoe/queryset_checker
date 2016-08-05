from django import forms

from checker.models import Query


class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        exclude = ['date', 'status']
