from django import forms
from .models import ProductComments


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = ProductComments
        fields = ['content']
