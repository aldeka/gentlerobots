from django import forms
from bmarks.models import Bookmark

class BookmarkForm(forms.Form):
    tags = forms.CharField()
    url = forms.URLField(label="URL")
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
