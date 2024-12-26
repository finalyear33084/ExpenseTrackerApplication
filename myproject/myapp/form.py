from django import forms

from .models import ComplaintTable
class AddReplyForm(forms.ModelForm):
    class Meta:
        model=ComplaintTable
        fields=['Reply']
        