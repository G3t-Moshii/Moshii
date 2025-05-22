from django import forms

class SolutionForm(forms.Form):
    answer = forms.CharField(label='Your Answer', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
